#!/usr/bin/env python3
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

DASH_LINE_RE = re.compile(r"^\s*-{10,}\s*$")
API_CODE_DIV_RE = re.compile(r"<div\b[^>]*\bclass=\"api-code\"[^>]*>", re.IGNORECASE)
TABLE_RE = re.compile(r"<table\b[^>]*>.*?</table>", re.IGNORECASE | re.DOTALL)
TR_RE = re.compile(r"<tr\b[^>]*>.*?</tr>", re.IGNORECASE | re.DOTALL)
CELL_RE = re.compile(r"<t[dh]\b[^>]*>.*?</t[dh]>", re.IGNORECASE | re.DOTALL)
BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
TAG_RE = re.compile(r"(?<!\\)<[^>]+>")
A_TAG_RE = re.compile(r"<a\b[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", re.IGNORECASE | re.DOTALL)
FENCE_RE = re.compile(r"```")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]+\)")
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")


def strip_footer(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if DASH_LINE_RE.match(line):
            return "\n".join(lines[:i]).rstrip() + "\n"
    return text


def remove_non_python_api_divs(text: str) -> str:
    pos = 0
    out = []
    while True:
        match = API_CODE_DIV_RE.search(text, pos)
        if not match:
            out.append(text[pos:])
            break
        tag = text[match.start():match.end()]
        id_match = re.search(r"\bid=\"([^\"]+)\"", tag, re.IGNORECASE)
        div_id = (id_match.group(1) if id_match else "").strip().lower()
        end = text.find("</div>", match.end())
        if end == -1:
            out.append(text[pos:match.start()])
            pos = match.end()
            continue
        out.append(text[pos:match.start()])
        inner = text[match.end():end]
        if div_id == "python":
            cleaned_inner = strip_html_tags(inner)
            cleaned_inner = html.unescape(cleaned_inner).strip("\n")
            if "```" in cleaned_inner:
                out.append(cleaned_inner + "\n")
            else:
                out.append("```python\n")
                out.append(cleaned_inner.rstrip() + "\n")
                out.append("```\n")
        pos = end + len("</div>")
    return "".join(out)


def strip_html_tags(text: str) -> str:
    return TAG_RE.sub("", text)


def convert_links(text: str) -> str:
    def repl(match: re.Match) -> str:
        href = match.group(1).strip()
        label = strip_html_tags(match.group(2)).strip()
        return f"[{label}]({href})" if label else href

    return A_TAG_RE.sub(repl, text)


def normalize_cell_text(cell_html: str) -> str:
    text = BR_RE.sub(" ", cell_html)
    text = convert_links(text)
    text = strip_html_tags(text)
    text = html.unescape(text)
    text = " ".join(text.split())
    return text


def table_to_markdown(table_html: str) -> str:
    rows = []
    header_index = None
    for row_html in TR_RE.findall(table_html):
        is_header = bool(re.search(r"<th\b", row_html, re.IGNORECASE)) or (
            re.search(r"class=\"[^\"]*header[^\"]*\"", row_html, re.IGNORECASE) is not None
        )
        cells = [normalize_cell_text(c) for c in CELL_RE.findall(row_html)]
        if not cells:
            continue
        if is_header and header_index is None:
            header_index = len(rows)
        rows.append(cells)

    if not rows:
        return ""

    max_cols = max(len(r) for r in rows)
    rows = [r + [""] * (max_cols - len(r)) for r in rows]

    if header_index is None:
        header_index = 0

    header = rows.pop(header_index)
    if all(not c for c in header) and rows:
        header = rows.pop(0)

    def escape_cell(cell: str) -> str:
        return cell.replace("|", "\\|")

    header_line = "| " + " | ".join(escape_cell(c) for c in header) + " |"
    separator_line = "| " + " | ".join(["---"] * len(header)) + " |"
    body_lines = ["| " + " | ".join(escape_cell(c) for c in row) + " |" for row in rows]

    lines = [header_line, separator_line] + body_lines
    return "\n".join(lines) + "\n"


def convert_html_tables(text: str) -> str:
    def repl(match: re.Match) -> str:
        return table_to_markdown(match.group(0))

    return TABLE_RE.sub(repl, text)

def normalize_fence_boundaries(text: str) -> str:
    def insert_newline_before(match: re.Match) -> str:
        prefix = match.group(1)
        return f"{prefix}\n```"

    text = re.sub(r"([^\n])```", insert_newline_before, text)
    return text

def remove_tabs_links(text: str) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped in ("- [Python](#Python)", "- [C++](#C++)", "- [TypeScript](#TypeScript)"):
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def apply_outside_code(text: str, transform) -> str:
    lines = text.splitlines(keepends=True)
    fence_indexes = [i for i, line in enumerate(lines) if line.lstrip().startswith("```")]
    ignored_fences = set()
    if len(fence_indexes) % 2 == 1 and fence_indexes:
        ignored_fences.add(fence_indexes[0])

    out = []
    buf = []
    in_code = False

    for idx, line in enumerate(lines):
        is_fence = line.lstrip().startswith("```") and idx not in ignored_fences
        if in_code:
            out.append(line)
            if is_fence:
                in_code = False
            continue
        if is_fence:
            if buf:
                out.append(transform("".join(buf)))
                buf = []
            in_code = True
            out.append(line)
            continue
        buf.append(line)

    if buf:
        out.append(transform("".join(buf)))

    return "".join(out)


def remove_non_python_code_blocks(text: str) -> str:
    def is_code_line(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.endswith("*/"):
            return True
        if stripped.endswith(";"):
            return True
        if "->" in stripped or "::" in stripped:
            return True
        if "{" in stripped or "}" in stripped:
            return True
        if re.search(r"\\b#include\\b", stripped):
            return True
        if re.search(r"\\bstd::", stripped):
            return True
        if re.search(r"\\bPtr\\b", stripped):
            return True
        if re.search(r"\\b(class|struct|namespace|bool)\\b", stripped):
            return True
        return False

    def should_remove_block(block: list[str]) -> bool:
        nonblank = [line for line in block if line.strip()]
        if len(nonblank) < 8:
            return False
        code_lines = sum(1 for line in nonblank if is_code_line(line))
        return code_lines >= 4 and (code_lines / len(nonblank)) >= 0.4

    lines = text.splitlines()
    out = []
    block = []
    code_lines = 0
    nonblank = 0
    in_block = False

    def reset_block() -> None:
        nonlocal block, code_lines, nonblank, in_block
        block = []
        code_lines = 0
        nonblank = 0
        in_block = False

    def flush_block() -> None:
        nonlocal block
        if not block:
            return
        if should_remove_block([line for line in block if line.strip()]):
            reset_block()
            return
        out.extend(block)
        reset_block()

    for line in lines:
        stripped = line.lstrip()
        is_stop = stripped.startswith("#") or stripped.startswith("- ") or stripped.startswith("* ") or stripped.startswith("|")
        if is_stop:
            flush_block()
            out.append(line)
            continue

        if not line.strip():
            if in_block:
                block.append(line)
            else:
                out.append(line)
            continue

        line_is_code = is_code_line(line)
        if line_is_code and not in_block:
            in_block = True

        if in_block:
            block.append(line)
            nonblank += 1
            if line_is_code:
                code_lines += 1
            continue

        out.append(line)

    flush_block()
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def strip_html_outside_code(text: str) -> str:
    return apply_outside_code(text, strip_html_tags)


def convert_links_outside_code(text: str) -> str:
    return apply_outside_code(text, convert_links)


def remove_non_python_blocks_outside_code(text: str) -> str:
    return apply_outside_code(text, remove_non_python_code_blocks)

def unescape_newlines_outside_code(text: str) -> str:
    return apply_outside_code(text, lambda t: t.replace("\\n", "\n"))

def remove_non_python_fenced_blocks(text: str) -> str:
    lines = text.splitlines(keepends=True)
    out = []
    in_code = False
    fence_line = ""
    code_lines = []

    def is_python_code(fence: str, code: str) -> bool:
        fence_lower = fence.lower()
        if fence_lower.startswith("```python") or fence_lower.startswith("``` api-code"):
            return True
        python_markers = ["import ", "def ", "self", "None", "True", "False", "adsk."]
        if any(marker in code for marker in python_markers):
            return True
        cpp_markers = ["#include", "std::", "->", "::", "Ptr ", "bool ", "class ", "struct "]
        if any(marker in code for marker in cpp_markers):
            return False
        return False

    for line in lines:
        if line.lstrip().startswith("```"):
            if not in_code:
                in_code = True
                fence_line = line
                code_lines = []
            else:
                code_text = "".join(code_lines)
                if is_python_code(fence_line, code_text):
                    out.append("```python\n")
                    out.extend(code_lines)
                    out.append("```\n")
                in_code = False
                fence_line = ""
                code_lines = []
            continue
        if in_code:
            code_lines.append(line)
        else:
            out.append(line)

    if in_code:
        out.append(fence_line)
        out.extend(code_lines)

    return "".join(out)

def normalize_markdown_links_outside_code(text: str) -> str:
    def normalize(chunk: str) -> str:
        def repl(match: re.Match) -> str:
            label = match.group(1)
            href = match.group(2)
            if href.lower().startswith("mailto:"):
                return label
            if href.endswith(".htm"):
                candidate = Path(href).with_suffix(".md").name
                if (ROOT / candidate).exists():
                    href = candidate
            return f"[{label}]({href})"

        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, chunk)

    return apply_outside_code(text, normalize)

def remove_markdown_images_outside_code(text: str) -> str:
    return apply_outside_code(text, lambda t: MD_IMAGE_RE.sub("", t))

def remove_boilerplate_lines(text: str) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        if line.startswith("Defined in namespace "):
            continue
        if line.startswith("Defined in namespace"):
            continue
        if "and the header file is" in line and "Defined in namespace" in line:
            continue
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def unescape_text_outside_code(text: str) -> str:
    def unescape(chunk: str) -> str:
        chunk = chunk.replace("\\<", "<").replace("\\>", ">")
        return html.unescape(chunk)

    return apply_outside_code(text, unescape)

def remove_empty_syntax_sections(text: str) -> str:
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "## Syntax":
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            content = [line for line in lines[i + 1 : j] if line.strip()]
            if not content:
                i = j
                continue
        out.append(lines[i])
        i += 1
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def remove_markdown_links_in_pythonish_lines(text: str) -> str:
    lines = text.splitlines()
    out = []

    for line in lines:
        stripped = line.lstrip()
        is_pythonish = (
            stripped.startswith(("if ", "for ", "while ", "def ", "class ", "import ", "from ", "try:", "except", "with "))
            or line.startswith(("    ", "\t"))
            or stripped.startswith("#")
        )
        if is_pythonish and MD_LINK_RE.search(line):
            continue
        out.append(line)

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

def collapse_blank_lines_outside_code(text: str) -> str:
    def collapse(chunk: str) -> str:
        lines = chunk.splitlines()
        out = []
        blank = False
        for line in lines:
            if line.strip() == "":
                if blank:
                    continue
                blank = True
                out.append("")
                continue
            blank = False
            out.append(line)
        return "\n".join(out) + ("\n" if chunk.endswith("\n") else "")

    return apply_outside_code(text, collapse)


def fix_empty_markdown_headers(text: str) -> str:
    lines = text.splitlines()
    out = []
    i = 0
    sep_re = re.compile(r"^\|[\s:\-\|]+\|\s*$")

    while i < len(lines):
        line = lines[i]
        if line.startswith("|") and i + 1 < len(lines) and sep_re.match(lines[i + 1]):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(c == "" for c in cells):
                if i + 2 < len(lines) and lines[i + 2].startswith("|"):
                    out.append(lines[i + 2])
                    out.append(lines[i + 1])
                    i += 3
                    continue
                i += 2
                continue
        out.append(line)
        i += 1

    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def clean_text(text: str) -> str:
    text = normalize_fence_boundaries(text)
    text = unescape_newlines_outside_code(text)
    text = strip_footer(text)
    text = remove_non_python_api_divs(text)
    text = remove_tabs_links(text)
    text = remove_non_python_fenced_blocks(text)
    text = remove_markdown_links_in_pythonish_lines(text)
    text = convert_html_tables(text)
    text = convert_links_outside_code(text)
    text = normalize_markdown_links_outside_code(text)
    text = remove_markdown_images_outside_code(text)
    text = BR_RE.sub(" ", text)
    text = strip_html_outside_code(text)
    text = unescape_text_outside_code(text)
    text = remove_boilerplate_lines(text)
    text = remove_empty_syntax_sections(text)
    text = fix_empty_markdown_headers(text)
    text = collapse_blank_lines_outside_code(text)
    return text


def extract_section_items(lines: list[str], heading: str) -> list[tuple[str, str]]:
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
            break
    if start is None:
        return []
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    items = []
    seen = set()
    for line in lines[start:end]:
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
            name = match.group(1).strip()
            href = match.group(2).strip()
            if href.endswith(".htm"):
                candidate = Path(href).with_suffix(".md").name
                if (ROOT / candidate).exists():
                    href = candidate
            key = (name, href)
            if key in seen:
                continue
            seen.add(key)
            items.append(key)
    return items


def extract_namespace(text: str) -> str | None:
    for line in text.splitlines():
        if "Defined in namespace" in line:
            match = re.search(r"Defined in namespace \"([^\"]+)\"", line)
            if match:
                return match.group(1).strip()
    return None


def build_index(paths: list[Path], namespaces: dict[Path, str]) -> str:
    sections = []
    for path in sorted(paths):
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        title = None
        namespace = namespaces.get(path)
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title or not namespace:
            continue
        methods = extract_section_items(lines, "## Methods")
        properties = extract_section_items(lines, "## Properties")
        if not methods and not properties:
            continue
        heading = f"## [{title}]({path.name}) ({namespace})"
        parts = [heading]
        if methods:
            parts.append("**Methods**")
            parts.extend([f"- [{name}]({href})" for name, href in methods])
        if properties:
            parts.append("**Properties**")
            parts.extend([f"- [{name}]({href})" for name, href in properties])
        sections.append("\n".join(parts))

    header = "# API Index\n\n"
    return header + "\n\n".join(sections) + "\n"


def main() -> None:
    paths = sorted(p for p in ROOT.glob("*.md") if p.name != "INDEX.md")
    namespaces: dict[Path, str] = {}
    for path in paths:
        original = path.read_text(encoding="utf-8")
        namespace = extract_namespace(original)
        if namespace:
            namespaces[path] = namespace
        cleaned = clean_text(original)
        if cleaned != original:
            path.write_text(cleaned, encoding="utf-8")
    index_path = ROOT / "INDEX.md"
    index_path.write_text(build_index(paths, namespaces), encoding="utf-8")


if __name__ == "__main__":
    main()
