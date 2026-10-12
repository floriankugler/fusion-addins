"""Values typed as literals are checked at run time too: a build also runs
without the type checker (the preview rebuilds on every save), and a
misspelt value must end in a LangError that names the call and the values
it takes, not in a KeyError or in silence."""
import pytest

from lang import *
from helpers import ply15

BOX = Box.from_size(width=600, depth=500, height=720)


@pytest.mark.parametrize("call, message", [
    (lambda: BOX.split("hight", 3), "split(): expected 'width', 'depth' or 'height', not 'hight'."),   # type: ignore[arg-type]
    (lambda: BOX.extent("lenght"), "extent(): expected"),                                             # type: ignore[arg-type]
    (lambda: BOX.center("wide"), "center(): expected"),                                               # type: ignore[arg-type]
    (lambda: to("iner"), "to(): expected 'inner' or 'outer', not 'iner'."),                           # type: ignore[arg-type]
    (lambda: domino("4x30", count=2), "domino(): expected '4x20', "),                                 # type: ignore[arg-type]
    (lambda: domino("4x20", count=2, marks="ends"), "domino(marks=): expected 'all' or 'middle'"),    # type: ignore[arg-type]
    (lambda: domino("4x20", count=2, face="iner"), "domino(face=): expected 'inner' or 'outer'"),     # type: ignore[arg-type]
    (lambda: clamex("P-12", count=2), "clamex(): expected 'P-10' or 'P-14', not 'P-12'."),            # type: ignore[arg-type]
    (lambda: cabineo("10", count=2), "cabineo(): expected '8', '12' or '8 M6', not '10'."),           # type: ignore[arg-type]
    (lambda: cabineo("8", count=2, surface="flat"), "cabineo(surface=): expected 'flush' or 'anti-break'"),  # type: ignore[arg-type]
    (lambda: cabineo("8 M6", count=2, insert="M8"), "cabineo(insert=): expected 'M6 x 12.3'"),        # type: ignore[arg-type]
    (lambda: tenons(count=2, width=50, dogbones="side"), "tenons(dogbones=): expected 'corner' or 'hidden'"),  # type: ignore[arg-type]
    (lambda: triangles(along="hight"), "triangles(along=): expected 'width', 'depth' or 'height'"),   # type: ignore[arg-type]
])
def test_a_misspelt_value_names_the_call_and_the_choices(call, message):  # type: ignore[no-untyped-def]
    with pytest.raises(LangError) as error:
        call()
    assert message in str(error.value)


def test_a_misspelt_face_or_extent_on_a_board_names_the_board():
    with module("m", BOX) as m:
        side = board("side", ply15).on(m.left)
        with pytest.raises(LangError, match=r"^m.side: show\(\): expected 'inner' or 'outer', not 'outter'.$"):
            side.show("outter")                                  # type: ignore[arg-type]
        with pytest.raises(LangError, match=r"^m.side: grain\(\): expected 'width', 'depth' or 'height'"):
            side.grain("hight")                                  # type: ignore[arg-type]
        with pytest.raises(LangError, match="Unknown direction 'fornt'"):
            side.face("fornt")


def test_valid_values_pass_unchanged():
    assert BOX.extent("height") == 720
    assert to("outer").face == "outer"
    assert tenons(count=2, width=50, dogbones="hidden").dogbones == "hidden"
