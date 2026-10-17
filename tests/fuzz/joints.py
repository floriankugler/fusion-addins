"""Random pairs of boards and joints between them, for fuzzing the joints
(`lang.joints`) as `boards.py` fuzzes the cutouts: a case is plain data,
built with the language's own calls, and checked from the outside.

A pair (`PairCase`) is a board that is met, the side, and a board that
meets it edge-on, the shelf: lying flat or standing, its end on the
side's face, of any size and thickness, anywhere along and across the
side, also hanging over its edges (the contact is what the side covers),
optionally between two sides. The side may have rounded corners and a
pocket where the shelf meets it or beside it, the shelf a pocket out
through its end; the shelf's end may be notched, which parts its contact. The joint is a Domino, Clamex, Cabineo, screws or
tenons with settings drawn from their ranges and a little beyond, made
from either board, and after tenons optionally a second joint in their
gaps or through them.

`run_pair` checks what every joint promises (design/joints.md): no
other error than a LangError; a refused join changes no board; a join
from the side equals the join from the shelf; an accepted one plans,
draws and meshes, leaves every board in one piece, lets no two boards
share material, cuts no blind pocket or hole as deep as its board,
sinks no countersink past a board's edge, names the join's line on every
operation it made in either board, and a connector's operations lie
within its contact; a Domino slot is the Domino's outline inset by
half of `undersize`. A join across a
pocket made before, in the side's face or the shelf's end where they meet,
is refused, and only such a one [Florian, 2026-10-13].
"""
from __future__ import annotations

import linecache
import math
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from hypothesis import strategies as st
from shapely.geometry import LineString
from shapely.geometry import box as shapely_box

from boards import _pipeline_problems  # pyright: ignore[reportPrivateUsage]
from fuzzing import floats, fresh, sizes
from lang import Box, LangError, Pos, Shape, board, sheet_material, module
from lang.core.contact import Contact
from lang.core.crossing import crossing
from lang.core.cutouts import circle_geometry
from lang.core.directions import Direction, current_frame
from lang.core.geometry import NARROWEST, parts_of, polygons_of
from lang.core.layout import build_layout
from lang.core.ops import Cut, EdgeOp, Hole, Op, Pocket, VGroove
from lang.core.part import ON_FACE_TOLERANCE, Board
from lib import connector_data as data
from lang.joints import box_joint, cabineo, clamex, domino, groove, half_lap, screws, tenons
from lang.joints.common import face_toward, touching
from lang.preview.mesh import FINE, mesh_part
from tests.helpers import overlap

#: How much material (mm3) two boards may share before it counts, and how
#: thick (mm) on average across the shared region's largest face: the
#: meshes' booleans leave a film where faces coincide (3.6e-6 thick over a
#: groove of 8.5 by 370 by 12 mm with no clearance).
SHARED = 0.01
FILM = 1e-4

JointKind = Literal["domino", "clamex", "cabineo", "screws", "tenons", "groove"]
AfterKind = Literal["screws gaps", "screws tenons", "clamex gaps", "cabineo gaps"]
Params = tuple[tuple[str, Any], ...]


@dataclass(frozen=True)
class JointSpec:
    """A joint as data: its kind and the factory's arguments; `at=` as
    fractions of the first contact's length, made positions on it."""
    kind: JointKind | AfterKind
    params: Params = ()
    at: tuple[float, ...] | None = None


@dataclass(frozen=True)
class PairCase:
    """A side (thick on y, from y 0) and a shelf meeting its +y face with
    an end, in a module large enough for both; sizes in mm, positions as
    fractions where they depend on other sizes."""
    side_t: float
    side_size: tuple[float, float]          # along x and z
    shelf_t: float
    standing: bool                          # the shelf thick on x (a divider), else on z
    along: tuple[float, float]              # its extent along the contact, fractions of the side's
    across: float                           # where its thickness starts, a fraction of the side's room
    reach: float                            # how far it runs away from the side, along y
    two_sides: bool                         # a second side at its other end
    rounded: float                          # the side's corners rounded, a fraction of its narrow size
    pocket: tuple[float, float, float] | None   # in the side's face, under the shelf: along, width, depth fractions
    notch: tuple[float, float, float] | None    # in the shelf's end: along, width fractions, depth mm
    joint: JointSpec
    after: JointSpec | None
    from_side: bool                         # the join made from the side, else from the shelf
    again: bool = False                     # join the pair once more with the same kind of joint
    pocket_shift: float = 0.0               # the side's pocket moved across, in shelf thicknesses
    end_pocket: tuple[float, float, float] | None = None    # in the shelf's face, out through its end at
                                                            # the side: along, width, depth fractions


# -- strategies --------------------------------------------------------------------------------

def _thickness() -> st.SearchStrategy[float]:
    """Mostly the sheet thicknesses a carcass has, now and then any."""
    return st.one_of(st.sampled_from([15.0, 18.0, 19.0, 22.0, 25.0]), st.sampled_from([15.0, 18.0, 22.0]),
                     st.sampled_from([6.0, 9.0, 12.0]), sizes(4, 40))


def _fractions(most: int) -> st.SearchStrategy[tuple[float, ...]]:
    """Positions along a contact as fractions: mostly well inside it, now
    and then at its ends or anywhere."""
    inner = st.lists(floats(0.15, 0.85), min_size=1, max_size=most, unique=True)
    anywhere = st.lists(floats(0.0, 1.0), min_size=1, max_size=most, unique=True)
    return st.one_of(inner, inner, anywhere).map(lambda xs: tuple(sorted(xs)))


#: A big face for a joint: mostly the default, now and then inner or outer.
_FACES = st.sampled_from([None, None, None, "inner", "outer"])


@st.composite
def _counted(draw: st.DrawFn, end_default: bool = True) -> tuple[Params, tuple[float, ...] | None]:
    """count= (with end= or not) or at= as fractions."""
    if draw(st.booleans()):
        count = draw(st.integers(1, 5))
        params: Params = (("count", count),)
        if count > 1 and (not end_default or draw(st.booleans())):
            params += (("end", draw(st.one_of(st.just(0.0), sizes(0, 120)))),)
        return params, None
    return (), draw(_fractions(4))


@st.composite
def joint_specs(draw: st.DrawFn) -> JointSpec:
    kind: JointKind = draw(st.sampled_from(["domino", "clamex", "cabineo", "screws", "tenons", "groove"]))
    face = draw(_FACES)
    if kind == "domino":
        counted, at = draw(_counted())
        params: Params = (("size", draw(st.one_of(st.sampled_from(["4x20", "5x30", "6x40"]),
                                                  st.sampled_from(["8x36", "8x50", "10x50", "12x100"])))),
                          *counted, ("face", face),
                          ("fence", draw(st.one_of(st.none(), st.none(), sizes(0, 20)))),
                          ("remaining", draw(st.one_of(st.none(), st.none(), sizes(0, 15)))),
                          ("loose", draw(st.sampled_from([0.0, 6.0, 10.0]))),
                          ("undersize", draw(st.one_of(st.just(0.2), st.just(0.0), floats(-1, 1)))),
                          ("marks", draw(st.sampled_from(["all", "middle", None]))),
                          ("mark_depth", draw(st.one_of(st.just(0.3), floats(0.1, 2)))))
        return JointSpec(kind, params, at)
    if kind == "clamex":
        counted, at = draw(_counted())
        return JointSpec(kind, (("model", draw(st.sampled_from(["P-10", "P-14"]))), *counted, ("face", face),
                                ("guide_d", draw(st.one_of(st.just(7.7), sizes(3, 12)))),
                                ("through", draw(st.booleans()))), at)
    if kind == "cabineo":
        counted, at = draw(_counted())
        model = draw(st.sampled_from(["8", "12", "8 M6"]))
        insert = draw(st.sampled_from([None, "M6 x 12.3", "M6 x 15.3", "threaded insert"])) if model == "8 M6" else None
        return JointSpec(kind, (("model", model), *counted, ("face", face), ("insert", insert),
                                ("surface", draw(st.sampled_from([None, "flush", "anti-break"]))),
                                ("through", draw(st.booleans()))), at)
    if kind == "screws":
        counted, at = draw(_counted())
        return JointSpec(kind, (("d", draw(st.one_of(st.just(4.0), sizes(2, 8)))), *counted,
                                ("countersink", draw(st.booleans()))), at)
    if kind == "groove":
        return JointSpec(kind, (("depth", draw(st.one_of(st.sampled_from([4.0, 5.0, 8.0]), sizes(0.5, 20)))),
                                ("clearance", (draw(st.sampled_from([0.0, 0.5, 1.0])),
                                               draw(st.sampled_from([0.0, 0.5, 1.0])))),
                                ("chamfer", draw(st.sampled_from([3.0, 0.0, None, 1.0]))),
                                ("dogbones", draw(st.sampled_from(["hidden", "corner", None]))),
                                ("tool", draw(st.sampled_from([6.0, 6.0, 3.0, 8.0]))),
                                ("relief", draw(st.sampled_from([0.1, 0.0, 0.5])))))
    # tenons
    how = draw(st.sampled_from(["count", "even", "at"]))
    common: Params = (("remaining", draw(st.one_of(st.just(0.0), sizes(0, 15)))),
                      ("clearance", (draw(st.sampled_from([0.0, 0.1, 0.3])), draw(st.sampled_from([0.0, 0.1, 0.3])))),
                      ("extra_depth", draw(st.one_of(st.just(0.5), sizes(0, 3)))),
                      ("tool", draw(st.sampled_from([6.0, 6.0, 3.0, 8.0, 0.0]))),
                      ("relief", draw(st.sampled_from([0.0, 0.1, 0.5]))),
                      ("dogbones", draw(st.sampled_from(["corner", "hidden", None]))))
    if how == "even":
        return JointSpec(kind, (("count", draw(st.integers(1, 5))), ("even", True), *common))
    width = draw(st.one_of(st.sampled_from([20.0, 50.0]), sizes(4, 150)))
    if how == "count":
        count = draw(st.integers(1, 4))
        margin: Params = (("margin", draw(sizes(0, 80))),) if count > 1 and draw(st.booleans()) else ()
        return JointSpec(kind, (("count", count), ("width", width), *margin, *common))
    return JointSpec(kind, (("width", width), *common), draw(_fractions(3)))


@st.composite
def after_specs(draw: st.DrawFn) -> JointSpec:
    kind: AfterKind = draw(st.sampled_from(["screws gaps", "screws tenons", "clamex gaps", "cabineo gaps"]))
    if kind.startswith("screws"):
        offset = draw(st.one_of(st.none(), sizes(1, 30)))
        return JointSpec(kind, (("d", draw(st.one_of(st.just(4.0), sizes(2, 8)))), ("offset", offset),
                                ("countersink", draw(st.booleans()))))
    if kind == "clamex gaps":
        return JointSpec(kind, (("model", draw(st.sampled_from(["P-10", "P-14"]))),))
    return JointSpec(kind, (("model", draw(st.sampled_from(["8", "12"]))),))


@st.composite
def pair_cases(draw: st.DrawFn) -> PairCase:
    joint = draw(joint_specs())
    after = draw(st.one_of(st.none(), after_specs())) if joint.kind == "tenons" else None
    return PairCase(
        side_t=draw(_thickness()),
        side_size=(draw(st.one_of(st.just(500.0), sizes(40, 1200))), draw(st.one_of(st.just(700.0), sizes(40, 1200)))),
        shelf_t=draw(_thickness()),
        standing=draw(st.booleans()),
        along=draw(st.one_of(st.just((0.0, 1.0)), st.tuples(floats(-0.2, 0.7), floats(0.3, 1.2)))),
        across=draw(st.one_of(st.just(0.5), floats(0.1, 0.9), floats(-0.05, 1.05))),
        reach=draw(st.one_of(st.just(400.0), sizes(30, 900))),
        two_sides=draw(st.booleans()),
        rounded=draw(st.one_of(st.just(0.0), floats(0.0, 0.45))),
        pocket=draw(st.one_of(st.none(), st.tuples(floats(0, 1), floats(0.02, 0.5), floats(0.1, 0.9)))),
        notch=draw(st.one_of(st.none(), st.tuples(floats(0, 1), floats(0.02, 0.6), sizes(1, 60)))),
        joint=joint, after=after, from_side=draw(st.booleans()), again=draw(st.booleans()),
        pocket_shift=draw(st.one_of(st.just(0.0), st.just(1.5), st.just(-1.5), floats(-3, 3))),
        end_pocket=draw(st.one_of(st.none(), st.none(), st.tuples(floats(0, 1), floats(0.02, 0.5), floats(0.1, 0.9)))))


# -- building -----------------------------------------------------------------------------------

#: The side starts this far in from the module's corner on x and z, so a
#: shelf hanging over its edges stays inside the module.
_IN = 300.0


@dataclass
class Built:
    side: Board
    shelf: Board
    other: Board | None                     # the second side
    extra: list[Board] = field(default_factory=list[Board])         # a frame's front and back
    named: dict[str, Board] = field(default_factory=dict[str, Board])

    @property
    def boards(self) -> list[Board]:
        return [b for b in (self.side, self.shelf, self.other) if b is not None] + self.extra


def build(case: PairCase, name: str = "m") -> Built:
    """The pair in a module named `name`, with the side's rounding and
    pocket and the shelf's notch; LangError when the language refuses it."""
    lx, lz = case.side_size
    far = case.side_t + case.reach
    width = far + (case.side_t if case.two_sides else 0.0) + 10
    with module(name, Box.from_size(width=width, depth=lx + 2 * _IN, height=lz + 2 * _IN)) as m:
        side = board("side", sheet_material("birch", t=case.side_t)).on(Pos("y", 0), toward=m.right).between(
            Pos("x", _IN), Pos("x", _IN + lx), Pos("z", _IN), Pos("z", _IN + lz))
        a0, a1 = sorted(case.along)
        if case.standing:                   # thick on x, along z
            length, room = lz, lx
        else:                               # thick on z, along x
            length, room = lx, lz
        lo, hi = _IN + a0 * length, _IN + max(a1, a0 + 0.02) * length
        start = _IN + case.across * (room - case.shelf_t)
        shelf = board("shelf", sheet_material("birch", t=case.shelf_t))
        if case.standing:
            shelf.on(Pos("x", start), toward=m.back).between(Pos("z", lo), Pos("z", hi), Pos("y", case.side_t),
                                                             Pos("y", far))
        else:
            shelf.on(Pos("z", start), toward=m.top).between(Pos("x", lo), Pos("x", hi), Pos("y", case.side_t),
                                                            Pos("y", far))
        other = None
        if case.two_sides:
            other = board("other", sheet_material("birch", t=case.side_t)).on(Pos("y", far), toward=m.right).between(
                Pos("x", _IN), Pos("x", _IN + lx), Pos("z", _IN), Pos("z", _IN + lz))
        if case.rounded > 0:
            r = case.rounded * min(lx, lz)
            if r > 0.5:
                side.fillet(face_toward(side, 1, "y").outline, r)
        if case.pocket is not None:
            at, w, d = case.pocket
            face = face_toward(side, 1, "y")
            u, v = side.u_axis, side.v_axis
            centre = {"x": start + case.shelf_t / 2, "z": (lo + hi) / 2} if case.standing else \
                {"x": (lo + hi) / 2, "z": start + case.shelf_t / 2}
            along_axis = "z" if case.standing else "x"
            centre[along_axis] = lo + at * (hi - lo)
            across_axis = "x" if case.standing else "z"
            centre[across_axis] += case.pocket_shift * case.shelf_t
            half = {along_axis: w * (hi - lo) / 2, across_axis: case.shelf_t}
            box = shapely_box(centre[u] - half[u], centre[v] - half[v], centre[u] + half[u], centre[v] + half[v])
            side.add_pocket(face, Shape(box), max(0.1, d * case.side_t), name="recess")
        if case.end_pocket is not None:
            at, w, d = case.end_pocket
            along_axis = "z" if case.standing else "x"
            mid = lo + at * (hi - lo)
            spans = {along_axis: (mid - w * (hi - lo) / 2, mid + w * (hi - lo) / 2),
                     "y": (case.side_t, case.side_t + min(20.0, case.reach / 3))}
            u, v = shelf.u_axis, shelf.v_axis
            shelf.add_pocket(face_toward(shelf, 1, shelf.t_axis),
                             Shape(shapely_box(spans[u][0], spans[v][0], spans[u][1], spans[v][1])),
                             max(0.1, d * case.shelf_t), name="end_recess")
        if case.notch is not None:
            at, w, d = case.notch
            u, v = shelf.u_axis, shelf.v_axis
            along_axis = "z" if case.standing else "x"
            spans = {along_axis: (lo + at * (hi - lo) - w * (hi - lo) / 2, lo + at * (hi - lo) + w * (hi - lo) / 2),
                     "y": (case.side_t - 1, case.side_t + d)}
            shelf.add_cut(Shape(shapely_box(spans[u][0], spans[v][0], spans[u][1], spans[v][1])))
    return Built(side, shelf, other)


def _positions(spec: JointSpec, contacts: list[Contact]) -> dict[str, Any]:
    """`at=` as positions along the first contact."""
    if spec.at is None or not contacts:
        return {}
    c = contacts[0]
    return {"at": [Pos(c.axis, c.lo + f * (c.hi - c.lo)) for f in spec.at]}


def make_joint(spec: JointSpec, contacts: list[Contact], first: Any = None) -> Any:
    """The joint the spec stands for (`first`, the tenons, for a joint in
    their gaps or through them)."""
    kwargs = dict(spec.params) | _positions(spec, contacts)
    if spec.kind == "domino":
        return domino(**kwargs)
    if spec.kind == "clamex":
        return clamex(**kwargs)
    if spec.kind == "cabineo":
        return cabineo(**kwargs)
    if spec.kind == "screws":
        return screws(**kwargs)
    if spec.kind == "tenons":
        return tenons(**kwargs)
    if spec.kind == "groove":
        depth = kwargs.pop("depth")
        return groove(depth, **kwargs)
    if spec.kind == "screws gaps":
        return screws(gaps=first, **kwargs)
    if spec.kind == "screws tenons":
        return screws(tenons=first, **kwargs)
    if spec.kind == "clamex gaps":
        return clamex(gaps=first, **kwargs)
    return cabineo(gaps=first, **kwargs)


class Refused(Exception):
    """A join refused, and whether it left the boards as they were."""

    def __init__(self, error: LangError, clean: bool):
        super().__init__(str(error))
        self.error, self.clean = error, clean


def _join(b: Built, spec: JointSpec, from_side: bool, first: Any = None) -> Any:
    """Makes the joint from the side(s), one join each, or from the shelf;
    the joint. A refusal raises `Refused`, which says whether that join
    (not the ones before it) changed nothing."""
    try:
        found = touching(b.shelf, b.side)
    except LangError:
        found = []              # (refused across a pocket: so is the join, below)
    joint = make_joint(spec, found, first)
    sides = [s for s in (b.side, b.other) if s is not None]
    calls = [(s, [b.shelf]) for s in sides] if from_side else [(b.shelf, sides)]
    for receiver, partners in calls:
        before = _state(b.boards)
        try:
            receiver.join(*partners, using=joint)
        except LangError as e:
            raise Refused(e, _state(b.boards) == before) from e
    return joint


# -- checking -----------------------------------------------------------------------------------

def _state(boards: list[Board]) -> list[tuple[str, str, list[Op]]]:
    return [(b.path, b.outline.geometry.wkt, list(b.ops)) for b in boards]


def run_pair(case: PairCase) -> list[str]:
    """What is wrong with the joint on the case's pair; [] when the pair or
    the joint is refused with a LangError that changed nothing."""
    with fresh():
        try:
            return _run_pair(case)
        except LangError:
            return []          # the pair itself refused (placing, rounding, a pocket or notch)
        except Exception as e:
            frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                          if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
            return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]


def _run_pair(case: PairCase) -> list[str]:
    b = build(case)
    pieces = {x.path: len(x.outline.polygons()) for x in b.boards}
    across = _across_made_before(case, b)
    if across is not False:
        # A join across a pocket made before is refused, and changes nothing.
        before = _state(b.boards)
        try:
            _join(b, case.joint, case.from_side)
        except Refused as refused:
            if not refused.clean:
                return [f"a {case.joint.kind} refused across a pocket changed a board: {refused.error}"]
            if across and "which was made before" not in str(refused.error):
                return [f"a {case.joint.kind} across a pocket made before is refused otherwise: {refused.error}"]
            return []
        except LangError:
            return []           # the joint's own settings refused
        return [f"a {case.joint.kind} across a pocket made before is accepted"] if across else []
    try:
        contacts = touching(b.shelf, b.side) + (touching(b.shelf, b.other) if b.other is not None else [])
    except LangError as e:
        if "which was made before" in str(e):
            return [f"refused across a pocket where none lies in the contact: {e}"]
        raise
    before = _state(b.boards)
    joints: list[Any] = []
    for spec, from_side in [(case.joint, case.from_side)] + ([(case.after, not case.from_side)] if case.after else []):
        try:
            joints.append(_join(b, spec, from_side, joints[0] if joints else None))
        except Refused as refused:
            if not refused.clean:
                return [f"a refused {spec.kind} changed a board: {refused.error}"]
            if not joints:
                return []           # (from both sides, the first side's join stays, as it should)
            break
        except LangError:
            return []           # the joint's own settings refused
    if _state(b.boards) == before:
        return ["an accepted join changed no board"]
    problems: list[str] = []
    if case.again and case.after is None:
        # A pair joined twice with one kind of joint is an error, and changes nothing.
        joined = _state(b.boards)
        try:
            _join(b, case.joint, not case.from_side)
            problems.append(f"the pair joined twice with {case.joint.kind} is accepted")
        except Refused as refused:
            if not refused.clean or _state(b.boards) != joined:
                problems.append(f"the second {case.joint.kind} refused changed a board: {refused.error}")
        except LangError:
            pass
        if problems:
            return problems
    meshes: dict[str, Any] = {}
    problems += _plan_problems(meshes)
    for x in b.boards:
        if len(x.outline.polygons()) != pieces[x.path]:
            problems.append(f"{x.path} came apart in {len(x.outline.polygons())} pieces")
        problems += _depth_problems(x, before)
    problems += _shared_problems(b, meshes)
    problems += _sink_problems(b, before)
    problems += _line_problems(b, before)
    if case.joint.kind in ("domino", "clamex", "cabineo", "screws"):
        problems += _within_problems(b, contacts, before)
        problems += _station_problems(case.joint, b, contacts, before)
    if case.joint.kind == "domino":
        problems += _domino_problems(case.joint, contacts, before)
    if case.joint.kind == "tenons" and not problems:
        problems += _tenon_problems(case, b, contacts, meshes)
    return problems + _symmetry_problems(case, b)      # last: it builds the pair again


def _across_made_before(case: PairCase, b: Built) -> bool | None:
    """Whether the case's pockets, made before the join, lie where the
    shelf meets the side, worked out from the outside: the side's in its
    face over a contact (the shelf's end on the side's material, pieces
    narrower than NARROWEST either way left out), the shelf's in its end
    there, `NARROWEST` deep; None when it is too near to tell."""
    if case.pocket is None and case.end_pocket is None:
        return False
    along_i = 1 if case.standing else 0         # the contact's axis in the side's (x, z) frame
    start = _IN + case.across * ((case.side_size[0] if case.standing else case.side_size[1]) - case.shelf_t)
    sv = (b.shelf.u_axis, b.shelf.v_axis).index("y")

    def shelf_point(y: float, a: float) -> tuple[float, float]:
        return (y, a) if sv == 0 else (a, y)

    # the shelf's end: where its outline has material just past y = side_t
    line = LineString([shelf_point(case.side_t + 1e-6, -1e9), shelf_point(case.side_t + 1e-6, 1e9)])
    spans = [(float(g.bounds[1 - sv]), float(g.bounds[3 - sv]))
             for g in parts_of(b.shelf.outline.geometry.intersection(line)) if g.length > 0]
    areas: list[float] = []
    side_pockets = [op.shape.geometry for op in b.side.ops if isinstance(op, Pocket) and op.name == "recess"]
    end_pockets = [op.shape.geometry for op in b.shelf.ops if isinstance(op, Pocket) and op.name == "end_recess"]
    for a0, a1 in spans:
        lo, hi = [0.0, 0.0], [0.0, 0.0]
        lo[along_i], hi[along_i] = a0, a1
        lo[1 - along_i], hi[1 - along_i] = start, start + case.shelf_t
        window = shapely_box(lo[0], lo[1], hi[0], hi[1])
        for piece in polygons_of(b.side.outline.geometry.intersection(window)):
            x0, z0, x1, z1 = piece.bounds
            if min(x1 - x0, z1 - z0) < NARROWEST:
                continue
            areas += [g.intersection(piece).area for g in side_pockets]
            p0 = shelf_point(case.side_t, piece.bounds[along_i])
            p1 = shelf_point(case.side_t + NARROWEST, piece.bounds[along_i + 2])
            strip = shapely_box(p0[0], p0[1], p1[0], p1[1])
            areas += [g.intersection(strip).area for g in end_pockets]
    if any(1e-7 < a < 1e-5 for a in areas):
        return None
    return any(a >= 1e-5 for a in areas)

#: What a join reports on purpose, which the layout lists as its problems.
_NOTES = ("where it shows unless something covers it",)


def _plan_problems(meshes: dict[str, Any] | None = None) -> list[str]:
    """`boards._pipeline_problems` but the notes a joint makes on purpose;
    the parts' meshes into `meshes`, when given."""
    return [p for p in _pipeline_problems(meshes) if not any(n in p for n in _NOTES)]


def _symmetry_problems(case: PairCase, b: Built) -> list[str]:
    """The same pair joined from the other board comes out the same."""
    if case.two_sides or case.after is not None:
        return []
    here = _state(b.boards)
    with fresh():
        twin = build(case, "m")
        try:
            _join(twin, case.joint, not case.from_side)
        except (Refused, LangError) as e:
            return [f"joined from the {'shelf' if case.from_side else 'side'} it is refused: {e}"]
        there = _state(twin.boards)
    if [(p, w, sorted(map(repr, ops))) for p, w, ops in here] != [(p, w, sorted(map(repr, ops))) for p, w, ops in there]:
        return ["joined from the other board it comes out otherwise"]
    return []


def _new_ops(x: Board, before: list[tuple[str, str, list[Op]]]) -> list[Op]:
    old = next(ops for p, _, ops in before if p == x.path)
    return x.ops[len(old):] if x.ops[:len(old)] == old else list(x.ops)


def _line_problems(b: Built, before: list[tuple[str, str, list[Op]]]) -> list[str]:
    """Every operation the joins made, in either board, names the join
    call's line (`where`): a line of this file that calls `join(`."""
    problems: list[str] = []
    for x in b.boards:
        for op in _new_ops(x, before):
            file, _, line = op.where.rpartition(":")
            code = linecache.getline(file, int(line)) if line.isdigit() else ""
            if Path(file).name != "joints.py" or ".join(" not in code:
                problems.append(f"{x.path}: the {op.kind} {getattr(op, 'name', None)!r} a join made names "
                                f"{op.where!r}, not the join's line")
    return problems


def _depth_problems(x: Board, before: list[tuple[str, str, list[Op]]]) -> list[str]:
    """No blind pocket or hole a join made reaches its board's far face."""
    problems: list[str] = []
    for op in _new_ops(x, before):
        # (a depth given from the far face, a Domino's remaining=, means it)
        if isinstance(op, (Pocket, Hole)) and not (isinstance(op, Hole) and op.through) and \
                op.depth >= x.thickness - 1e-6 and op.depth_spec != "through" and not op.depth_spec.startswith("to("):
            problems.append(f"{x.path}: the {op.kind} {op.name!r} is {op.depth:g} deep in {x.thickness:g}")
    return problems


def _shared_problems(b: Built, meshes: dict[str, Any] | None = None) -> list[str]:
    """No two boards share material once joined."""
    meshes = meshes or _meshes()
    paths = [x.path for x in b.boards]
    # (a board in islands meshed open, which no boolean takes [fuzzing, 2026-10-13])
    problems = [f"{p}'s preview mesh is not a closed volume" for p in paths if not meshes[p].is_volume]
    if problems:
        return problems
    for i, p in enumerate(paths):
        for q in paths[i + 1:]:
            shared, face = _shared(meshes[p], meshes[q])
            if shared > max(SHARED, FILM * face):
                problems.append(f"{p} and {q} share {shared:.3g} mm3")
    return problems


def _shared(a: Any, b: Any) -> tuple[float, float]:
    """The volume two meshes share (mm3) and the area of the largest face
    of the box around it."""
    import warnings
    import trimesh
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        common = trimesh.boolean.intersection([a, b], engine="manifold")
        if not len(common.faces):
            return 0.0, 0.0
        e = sorted(float(x) for x in common.extents)
        return float(common.volume), e[1] * e[2]


def _within_problems(b: Built, contacts: list[Contact], before: list[tuple[str, str, list[Op]]]) -> list[str]:
    """A connector's or screw's operations lie within a contact: in the
    side's face along and across it, in the shelf's faces along it."""
    problems: list[str] = []
    for x in b.boards:
        for op in _new_ops(x, before):
            if isinstance(op, (EdgeOp, Cut)):
                problems.append(f"{x.path}: a connector made a {op.kind}")
                continue
            if isinstance(op, VGroove):
                continue
            # A hole by its bore: a countersink on the side's outer face may
            # be wider than the shelf is thick.
            region = circle_geometry((op.u, op.v), op.d / 2) if isinstance(op, Hole) else \
                x._footprint(op)  # pyright: ignore[reportPrivateUsage]
            if region.is_empty:
                continue
            # A Cabineo 8 M6's threaded-insert collar reaches past the
            # shelf's face by 1.35 mm, as in the add-in (design/joints.md, kept).
            collar = (getattr(op, "name", None) or "").endswith("_collar")
            fits = False
            for c in contacts:
                if x is c.face_on or x is c.edge_on:
                    lo, hi = _extent(x, region, c.axis)
                    if lo < c.lo - 1e-6 or hi > c.hi + 1e-6:
                        continue
                    if x is c.face_on and not collar:
                        alo, ahi = _extent(x, region, c.across)
                        if alo < c.across_lo - 1e-6 or ahi > c.across_hi + 1e-6:
                            continue
                    fits = True
            if not fits:
                problems.append(f"{x.path}: the {op.kind} {getattr(op, 'name', None)!r} lies outside every contact")
    return problems


def _domino_problems(spec: JointSpec, contacts: list[Contact], before: list[tuple[str, str, list[Op]]]) -> list[str]:
    """Every Domino slot is the Domino's outline inset by half of
    `undersize` (0.2 by default) on every side: its thickness less the
    undersize across the contact, its width less the undersize along it,
    and with `loose=` all but one per contact that much longer."""
    params = dict(spec.params)
    size = data.domino_size(params["size"])
    undersize = params.get("undersize", data.DOMINO_SLOT_UNDERSIZE)
    loose = params.get("loose", 0.0)
    height, length = size.thickness - undersize, size.width - undersize
    problems: list[str] = []
    for c in contacts:
        x = c.face_on
        lengths: list[float] = []
        for op in _new_ops(x, before):
            if not isinstance(op, Pocket):
                continue
            region = x._footprint(op)  # pyright: ignore[reportPrivateUsage]
            lo, hi = _extent(x, region, c.axis)
            if not c.lo - 1e-6 <= (lo + hi) / 2 <= c.hi + 1e-6:
                continue
            alo, ahi = _extent(x, region, c.across)
            if abs(ahi - alo - height) > 1e-6:
                problems.append(f"{x.path}: the slot {op.name!r} is {ahi - alo:.6g} high, not {height:.6g}")
            lengths.append(hi - lo)
        exact = [n for n in lengths if abs(n - length) <= 1e-6]
        others = [n for n in lengths if abs(n - length - loose) <= 1e-6]
        if lengths and not (len(exact) == len(lengths) if loose == 0 else
                            len(exact) == 1 and len(others) == len(lengths) - 1):
            wanted = f"all {length:.6g}" if loose == 0 else f"one {length:.6g} and the others {loose:g} longer"
            problems.append(f"{x.path}: the slots are {[round(n, 6) for n in lengths]} long, not {wanted}")
    return problems


def _sink_problems(b: Built, before: list[tuple[str, str, list[Op]]]) -> list[str]:
    """Every countersink a join made lies on its board's face: within the
    outline, give or take `ON_FACE_TOLERANCE` (Fusion cannot cut one
    reaching past the board's edge, 2026-10-13)."""
    problems: list[str] = []
    for x in b.boards:
        material = x.outline.geometry.buffer(ON_FACE_TOLERANCE)
        for op in _new_ops(x, before):
            if isinstance(op, Hole) and op.chamfer > 0 and \
                    not material.contains(circle_geometry((op.u, op.v), op.d / 2 + op.chamfer)):
                problems.append(f"{x.path}: the countersink of {op.name!r} reaches past the board's outline")
    return problems


def _extent(x: Board, region: Any, axis: str) -> tuple[float, float]:
    """A footprint's extent along a world axis of the board's plane."""
    x0, y0, x1, y1 = region.bounds
    return (x0, x1) if axis == x.u_axis else (y0, y1)


# -- box joints: a corner ------------------------------------------------------------------------

@dataclass(frozen=True)
class CornerCase:
    """A side (thick on y, from y 0) and a front meeting its +y face with
    an end, the front's outer face (thick on x) in the plane of the side's
    end, as at a drawer box's corner; `offset` moves the front off that
    plane (0: flush), `low` and `high` its height within the side's."""
    side_t: float
    front_t: float
    length: float                           # the side along x
    height: float                           # the side along z
    low: float                              # the front's height, fractions of the side's
    high: float
    reach: float                            # the front along y
    offset: float                           # the front's outer face off the side's end, mm
    at_far_end: bool                        # the corner at the side's far end on x
    two_sides: bool                         # a second side at the front's other end
    fingers: int
    margin: float
    tool: float
    clearance: tuple[float, float]
    from_side: bool


@st.composite
def corner_cases(draw: st.DrawFn) -> CornerCase:
    low = draw(st.one_of(st.just(0.0), floats(0, 0.5)))
    return CornerCase(
        side_t=draw(_thickness()), front_t=draw(_thickness()),
        length=draw(st.one_of(st.just(500.0), sizes(60, 900))), height=draw(st.one_of(st.just(150.0), sizes(20, 400))),
        low=low, high=draw(st.one_of(st.just(1.0), floats(low + 0.05, 1.0))),
        reach=draw(st.one_of(st.just(400.0), sizes(40, 800))),
        offset=draw(st.one_of(st.just(0.0), st.just(0.0), floats(-5, 5))),
        at_far_end=draw(st.booleans()), two_sides=draw(st.booleans()),
        fingers=draw(st.one_of(st.sampled_from([3, 5, 7, 9]), st.integers(1, 15))),
        margin=draw(st.one_of(st.just(0.0), st.just(2.0), sizes(0, 40))),
        tool=draw(st.sampled_from([6.0, 6.0, 0.0, 3.0, 8.0])),
        clearance=(draw(st.sampled_from([0.0, 0.1, 0.3])), draw(st.sampled_from([0.0, 0.1, 0.3]))),
        from_side=draw(st.booleans()))


def build_corner(case: CornerCase, name: str = "m") -> Built:
    far = case.side_t + case.reach
    width = far + (case.side_t if case.two_sides else 0.0) + 10
    with module(name, Box.from_size(width=width, depth=case.length + 2 * _IN, height=case.height + 2 * _IN)) as m:
        side = board("side", sheet_material("birch", t=case.side_t)).on(Pos("y", 0), toward=m.right).between(
            Pos("x", _IN), Pos("x", _IN + case.length), Pos("z", _IN), Pos("z", _IN + case.height))
        z0, z1 = _IN + case.low * case.height, _IN + case.high * case.height
        if case.at_far_end:
            x = _IN + case.length + case.offset
            front = board("front", sheet_material("birch", t=case.front_t)).on(Pos("x", x), toward=m.front)
        else:
            x = _IN - case.offset
            front = board("front", sheet_material("birch", t=case.front_t)).on(Pos("x", x), toward=m.back)
        front.between(Pos("z", z0), Pos("z", z1), Pos("y", case.side_t), Pos("y", far))
        other = None
        if case.two_sides:
            other = board("other", sheet_material("birch", t=case.side_t)).on(Pos("y", far), toward=m.right).between(
                Pos("x", _IN), Pos("x", _IN + case.length), Pos("z", _IN), Pos("z", _IN + case.height))
    return Built(side, front, other)


def _box(case: CornerCase) -> Any:
    return box_joint(case.fingers, margin=case.margin, tool=case.tool, clearance=case.clearance)


def run_corner(case: CornerCase) -> list[str]:
    """What is wrong with a box joint at the case's corner."""
    def make(name: str) -> Built:
        return build_corner(case, name)

    def join(b: Built, from_side: bool) -> None:
        _join_with(b, _box(case), from_side)

    def fill(b: Built, meshes: dict[str, Any]) -> list[str]:
        # The corner block: the front's thickness, through the side, the front's height.
        fb, sb = b.shelf.box(), b.side.box()
        lo = [fb.lo["x"], sb.lo["y"], fb.lo["z"]]
        hi = [fb.hi["x"], sb.hi["y"], fb.hi["z"]]
        n, r = case.fingers, case.tool / 2
        allowed = case.clearance[0] * (n + 1) * case.side_t * case.front_t \
            + 8 * (n + 1) * r * r * max(case.side_t, case.front_t)
        return _fill_problems(meshes, (b.side.path, b.shelf.path), lo, hi, allowed)

    return _guarded(lambda: _run_joined(make, join, case.from_side, not case.two_sides, fill))


# -- half laps: crossing boards ------------------------------------------------------------------

@dataclass(frozen=True)
class CrossCase:
    """Two boards standing on edge, crossing as an egg crate's dividers do:
    `a` thick on x, running along y, `b` thick on y, running along x, each
    from `z0` to `z1` (fractions of the module's height); `ends` moves
    each board's far end in, so it may stop inside the other or short of
    it."""
    a_t: float
    b_t: float
    a_z: tuple[float, float]
    b_z: tuple[float, float]
    a_at: float                             # where a lies along x, a fraction of b's length
    b_at: float                             # where b lies along y, a fraction of a's length
    ends: tuple[float, float]               # a's and b's far ends, fractions of their length
    second: bool                            # a second board crossing a, parallel to b
    toward_top: bool
    split: float | None                     # a fraction of the height they share
    clearance: float
    dogbones: Any
    tool: float
    relief: float


@st.composite
def cross_cases(draw: st.DrawFn) -> CrossCase:
    def zs() -> tuple[float, float]:
        lo = draw(st.one_of(st.just(0.0), floats(0, 0.6)))
        return lo, draw(st.one_of(st.just(1.0), floats(lo + 0.05, 1.0)))
    return CrossCase(
        a_t=draw(_thickness()), b_t=draw(_thickness()), a_z=zs(), b_z=zs(),
        a_at=draw(st.one_of(st.just(0.5), floats(0.05, 0.95))), b_at=draw(st.one_of(st.just(0.5), floats(0.05, 0.95))),
        ends=(draw(st.one_of(st.just(1.0), floats(0.3, 1.0))), draw(st.one_of(st.just(1.0), floats(0.3, 1.0)))),
        second=draw(st.booleans()), toward_top=draw(st.booleans()),
        split=draw(st.one_of(st.none(), st.none(), floats(-0.1, 1.1))),
        clearance=draw(st.sampled_from([0.0, 0.0, 0.2, 1.0])),
        dogbones=draw(st.sampled_from(["corner", "hidden", None])),
        tool=draw(st.sampled_from([6.0, 6.0, 3.0, 8.0])), relief=draw(st.sampled_from([0.1, 0.0, 0.5])))


#: The crossing boards' module: x by y by z, mm.
_CROSS = (600.0, 600.0, 200.0)


def build_cross(case: CrossCase, name: str = "m") -> Built:
    lx, ly, lz = _CROSS
    with module(name, Box.from_size(width=ly, depth=lx, height=lz)) as m:
        ax = case.a_at * (lx - case.a_t)
        a = board("a", sheet_material("birch", t=case.a_t)).on(Pos("x", ax), toward=m.back).between(
            Pos("y", 0), Pos("y", case.ends[0] * ly), Pos("z", case.a_z[0] * lz), Pos("z", case.a_z[1] * lz))
        by = case.b_at * (ly - case.b_t)
        b = board("b", sheet_material("birch", t=case.b_t)).on(Pos("y", by), toward=m.right).between(
            Pos("x", 0), Pos("x", case.ends[1] * lx), Pos("z", case.b_z[0] * lz), Pos("z", case.b_z[1] * lz))
        other = None
        if case.second:
            y2 = (by + case.b_t + ly) / 2
            if y2 + case.b_t <= ly:
                other = board("c", sheet_material("birch", t=case.b_t)).on(Pos("y", y2), toward=m.right).between(
                    Pos("x", 0), Pos("x", case.ends[1] * lx), Pos("z", case.b_z[0] * lz), Pos("z", case.b_z[1] * lz))
    return Built(b, a, other)


def _lap(case: CrossCase, a: Board) -> Any:
    split = None
    if case.split is not None:
        lo, hi = max(case.a_z[0], case.b_z[0]) * _CROSS[2], min(case.a_z[1], case.b_z[1]) * _CROSS[2]
        split = Pos("z", lo + case.split * (hi - lo))
    toward: Direction = current_frame().direction("top" if case.toward_top else "bottom")
    return half_lap(toward, split=split, clearance=case.clearance, dogbones=case.dogbones, tool=case.tool,
                    relief=case.relief)


def _ending_inside(b: Built) -> list[str]:
    """Where a board of the crossing ends inside the other, short of its
    far face, which a half lap refuses [Florian, 2026-10-13]."""
    found: list[str] = []
    for other in (b.side, b.other):
        if other is None or crossing(b.shelf, other) is None:
            continue
        for one, two in ((b.shelf, other), (other, b.shelf)):
            t = two.t_axis
            band, reach = two.box(), one.box()
            short = max(0.0, reach.lo[t] - band.lo[t]) + max(0.0, band.hi[t] - reach.hi[t])
            if short > 1e-6:
                found.append(f"{one.path} ends inside {two.path}, {short:.3g} short of its far face")
    return found

def run_cross(case: CrossCase) -> list[str]:
    """What is wrong with a half lap of the case's crossing boards (made
    from `a`, its notches toward `toward`)."""
    def make(name: str) -> Built:
        return build_cross(case, name)

    def join(b: Built, _: bool) -> None:
        inside = _ending_inside(b)
        try:
            b.shelf.join(*[x for x in (b.side, b.other) if x is not None], using=_lap(case, b.shelf))
        except LangError as e:
            if "ends inside" in str(e) and not inside:
                raise AssertionError(f"a lap refused where no board ends inside the other: {e}") from e
            raise
        if inside:
            raise AssertionError(f"a lap accepted where {inside[0]}")

    def fill(b: Built, meshes: dict[str, Any]) -> list[str]:
        problems: list[str] = []
        for other in (b.side, b.other):
            if other is None:
                continue
            cross = crossing_before.get(other.path)
            if cross is None:
                continue
            ab, ob = b.shelf.box(), other.box()
            # Where both boxes are: a board may end inside the other.
            lo = [max(ab.lo["x"], ob.lo["x"]), max(ab.lo["y"], ob.lo["y"]), cross[0]]
            hi = [min(ab.hi["x"], ob.hi["x"]), min(ab.hi["y"], ob.hi["y"]), cross[1]]
            r = (case.tool + case.relief) / 2 if case.dogbones is not None else 0.0
            allowed = case.clearance * (case.a_t + case.b_t) * (cross[1] - cross[0]) \
                + 4 * math.pi * r * r * max(case.a_t, case.b_t)
            problems += _fill_problems(meshes, (b.shelf.path, other.path), lo, hi, allowed)
        return problems

    crossing_before: dict[str, tuple[float, float]] = {}

    def make_and_note(name: str) -> Built:
        built = make(name)
        for other in (built.side, built.other):
            if other is not None:
                c = crossing(built.shelf, other)
                if c is not None:
                    crossing_before[other.path] = (c.lo, c.hi)
        return built

    return _guarded(lambda: _run_joined(make_and_note, join, False, False, fill))


# -- shared by the corner and the crossing -------------------------------------------------------

def _guarded(run: Any) -> list[str]:
    with fresh():
        try:
            return run()
        except LangError:
            return []
        except Exception as e:
            frame = next((fr for fr in reversed(traceback.extract_tb(e.__traceback__))
                          if "/lang/" in fr.filename), traceback.extract_tb(e.__traceback__)[-1])
            return [f"{type(e).__name__} at {Path(frame.filename).name}:{frame.lineno}: {e}"]


def _join_with(b: Built, joint: Any, from_side: bool) -> None:
    sides = [s for s in (b.side, b.other) if s is not None]
    if from_side:
        for s in sides:
            s.join(b.shelf, using=joint)
    else:
        b.shelf.join(*sides, using=joint)


def _run_joined(make: Any, join: Any, from_side: bool, symmetric: bool, fill: Any = None) -> list[str]:
    """Builds the boards, joins them; the generic promises of a join: a
    refusal changes nothing; accepted, it plans, draws and meshes, no
    board comes apart, no two share material, no blind pocket or hole is
    as deep as its board, and (with `symmetric`) the join from the other
    board comes out the same."""
    b: Built = make("m")
    pieces = {x.path: len(x.outline.polygons()) for x in b.boards}
    before = _state(b.boards)
    try:
        join(b, from_side)
    except Refused as refused:             # one of several joins: those before it stay
        return [] if refused.clean else [f"a refused join changed a board: {refused.error}"]
    except LangError:
        if _state(b.boards) != before:
            return ["a refused join changed a board"]
        return []
    if _state(b.boards) == before:
        return ["an accepted join changed no board"]
    meshes: dict[str, Any] = {}
    problems = _plan_problems(meshes)
    for x in b.boards:
        if len(x.outline.polygons()) != pieces[x.path]:
            problems.append(f"{x.path} came apart in {len(x.outline.polygons())} pieces")
        problems += _depth_problems(x, before)
    problems += _shared_problems(b, meshes)
    if fill is not None and not problems:
        problems += fill(b, meshes)
    if symmetric:
        here = _state(b.boards)
        with fresh():
            twin: Built = make("m")
            try:
                join(twin, not from_side)
            except LangError as e:
                return problems + [f"joined from the other board it is refused: {e}"]
            if [(p, w, sorted(map(repr, ops))) for p, w, ops in here] != \
                    [(p, w, sorted(map(repr, ops))) for p, w, ops in _state(twin.boards)]:
                problems.append("joined from the other board it comes out otherwise")
    return problems


# -- filling the joint ---------------------------------------------------------------------------

def _meshes() -> dict[str, Any]:
    layout = build_layout()
    return {p["path"]: mesh_part(p, layout["frame"], level=FINE) for m in layout["modules"] for p in m["parts"]}


def _volume_in(mesh: Any, lo: list[float], hi: list[float]) -> float:
    """How much of the mesh lies in the box from `lo` to `hi`."""
    import trimesh
    region = trimesh.creation.box(extents=[h - l for l, h in zip(lo, hi)])
    region.apply_translation([(l + h) / 2 for l, h in zip(lo, hi)])
    return overlap(mesh, region)


def _fill_problems(meshes: dict[str, Any], paths: tuple[str, str], lo: list[float], hi: list[float],
                   allowed: float) -> list[str]:
    """The two boards, which share no material, fill the box where they
    were joined but for `allowed` mm3 (clearances, dog bones, roundings)."""
    full = math.prod(h - l for l, h in zip(lo, hi))
    missing = full - sum(_volume_in(meshes[p], lo, hi) for p in paths)
    if missing > allowed + 1e-3 * full:
        return [f"the joint leaves {missing:.4g} mm3 of its {full:.4g} empty, more than {allowed:.4g}"]
    return []


# -- where the connectors go ---------------------------------------------------------------------

def _expected(spec: JointSpec, c: Contact, first: Contact) -> list[float]:
    """The stations along a contact as the joint's documented rule puts
    them, worked out here: `count=` from `lib.stations` with the outer ones
    `end` from the ends (37 for Dominos, 60 for the others by default),
    `at=` at the positions given (made on the first contact, the same for
    every contact)."""
    params = dict(spec.params)
    if spec.at is not None:
        return sorted(first.lo + f * (first.hi - first.lo) for f in spec.at)
    count = params["count"]
    end = params.get("end", data.DOMINO_STOP_LATCH if spec.kind == "domino" else data.DEFAULT_END_OFFSET)
    return [c.lo + x for x in data.stations(c.length, count, end)]


def _station_problems(spec: JointSpec, b: Built, contacts: list[Contact],
                      before: list[tuple[str, str, list[Op]]]) -> list[str]:
    """Every connector or screw the join made in the side sits at one of
    the stations, and every station has one: its centre along the contact
    (a Clamex's two guide holes 50.5 either side of it)."""
    offsets = [-data.CLAMEX_GUIDE_SPACING / 2, data.CLAMEX_GUIDE_SPACING / 2] if spec.kind == "clamex" else [0.0]
    problems: list[str] = []
    first = contacts[0] if contacts else None
    for side in (b.side, b.other):
        if side is None:
            continue
        mine = [c for c in contacts if c.face_on is side]
        stations = [s for c in mine for s in _expected(spec, c, first)] if first is not None else []
        centres: list[float] = []
        for op in _new_ops(side, before):
            if isinstance(op, (Hole, Pocket)) and mine:
                lo, hi = _extent(side, side._footprint(op), mine[0].axis)  # pyright: ignore[reportPrivateUsage]
                centres.append((lo + hi) / 2)
        wanted = [s + o for s in stations for o in offsets]
        stray = [x for x in centres if not any(abs(x - w) < 1e-6 for w in wanted)]
        missing = [w for w in wanted if not any(abs(x - w) < 1e-6 for x in centres)]
        if stray or missing:
            problems.append(f"{side.path}: the {spec.kind}s sit at {sorted(set(round(x, 3) for x in centres))}, "
                            f"the stations are {[round(w, 3) for w in wanted]}")
    return problems


# -- grooves: a panel in a frame -----------------------------------------------------------------

@dataclass(frozen=True)
class FrameCase:
    """A drawer box: sides `l` and `r` (thick on y) with a front `f` and a
    back `k` (thick on x) between them, all of one height, and a floor
    (thick on z) between their inner faces at `floor_at` (a fraction of
    the height); the floor joined with grooves to the boards in `into`,
    in one join or one board after another."""
    side_t: float
    end_t: float
    floor_t: float
    size: tuple[float, float, float]        # x, y, z outside
    floor_at: float
    into: tuple[str, ...]                   # of "l", "r", "f", "k"
    one_join: bool
    from_floor: bool
    depth: float
    clearance: tuple[float, float]
    chamfer: float | None
    dogbones: Any
    tool: float
    relief: float


@st.composite
def frame_cases(draw: st.DrawFn) -> FrameCase:
    into = draw(st.lists(st.sampled_from(["l", "r", "f", "k"]), min_size=1, max_size=4, unique=True))
    return FrameCase(
        side_t=draw(_thickness()), end_t=draw(_thickness()), floor_t=draw(st.one_of(st.sampled_from([6.0, 9.0, 12.0]),
                                                                                       sizes(3, 20))),
        size=(draw(st.one_of(st.just(500.0), sizes(80, 900))), draw(st.one_of(st.just(400.0), sizes(80, 900))),
              draw(st.one_of(st.just(150.0), sizes(40, 400)))),
        floor_at=draw(st.one_of(st.just(0.1), floats(0.0, 0.9))),
        into=tuple(sorted(into)), one_join=draw(st.booleans()), from_floor=draw(st.booleans()),
        depth=draw(st.one_of(st.sampled_from([4.0, 5.0, 8.0]), sizes(0.5, 15))),
        clearance=(draw(st.sampled_from([0.0, 0.5, 1.0])), draw(st.sampled_from([0.0, 0.5, 1.0]))),
        chamfer=draw(st.sampled_from([3.0, 0.0, None, 1.0, 8.0])),
        dogbones=draw(st.sampled_from(["hidden", "corner", None])),
        tool=draw(st.sampled_from([6.0, 6.0, 3.0, 8.0])), relief=draw(st.sampled_from([0.1, 0.0, 0.5])))


@dataclass
class Frame:
    boards: dict[str, Board]
    floor: Board


def build_frame(case: FrameCase, name: str = "m") -> Frame:
    lx, ly, lz = case.size
    with module(name, Box.from_size(width=ly, depth=lx, height=lz)) as m:
        l = board("l", sheet_material("birch", t=case.side_t)).on(m.left)
        r = board("r", sheet_material("birch", t=case.side_t)).on(m.right)
        f = board("f", sheet_material("birch", t=case.end_t)).on(m.front).between(l, r)
        k = board("k", sheet_material("birch", t=case.end_t)).on(m.back).between(l, r)
        z = case.floor_at * (lz - case.floor_t)
        floor = board("floor", sheet_material("birch", t=case.floor_t)).on(Pos("z", z), toward=m.top).between(l, r, f, k)
    return Frame({"l": l, "r": r, "f": f, "k": k}, floor)


def run_frame(case: FrameCase) -> list[str]:
    """What is wrong with a floor grooved into some of its box's boards."""
    def make(name: str) -> Built:
        fr = build_frame(case, name)
        return Built(fr.boards["l"], fr.floor, fr.boards["r"], [fr.boards["f"], fr.boards["k"]], fr.boards)

    def join(b: Built, _: bool) -> None:
        targets = [b.named[k] for k in case.into]
        joint = groove(case.depth, clearance=case.clearance, chamfer=case.chamfer, dogbones=case.dogbones,
                       tool=case.tool, relief=case.relief)
        if case.one_join and case.from_floor:
            calls = [(b.shelf, targets)]
        else:                              # one join per board: a later one at a corner an earlier one moved fails
            calls = [(b.shelf, [t]) if case.from_floor else (t, [b.shelf]) for t in targets]
        for receiver, partners in calls:
            ahead = _state(b.boards)
            try:
                receiver.join(*partners, using=joint)
            except LangError as e:
                raise Refused(e, _state(b.boards) == ahead) from e

    return _guarded(lambda: _run_joined(make, join, False, False))


# -- tenons ----------------------------------------------------------------------------------------

def _tenon_problems(case: PairCase, b: Built, contacts: list[Contact], meshes: dict[str, Any]) -> list[str]:
    """The tenons reach no further than the side's outer face, or than
    `remaining` short of it, and with the mortises they fill the contact's
    block through the side, but for the clearances and the dog bones."""
    params = dict(case.joint.params)
    remaining = params["remaining"]
    along, across = params["clearance"]
    r = (params["tool"] + params["relief"]) / 2 if params["dogbones"] is not None else 0.0
    problems: list[str] = []
    reach = min(y for poly in b.shelf.outline.polygons() for _, y in _yx(b.shelf, poly))
    if reach < remaining - 1e-6:
        problems.append(f"the tenons reach y={reach:g}, past the side's outer face less remaining={remaining:g}")
    if problems or case.after is not None or case.pocket is not None or case.rounded > 0:
        # (a second joint's holes, or the pocket, take material from the block too; with
        # rounded corners the contact's box reaches past the side's outline)
        return problems
    for c in contacts:
        if c.face_on is not b.side:
            continue
        lo = {c.axis: c.lo, c.across: c.across_lo, "y": remaining}
        hi = {c.axis: c.hi, c.across: c.across_hi, "y": case.side_t}
        box_lo, box_hi = [lo[a] for a in ("x", "y", "z")], [hi[a] for a in ("x", "y", "z")]
        full = math.prod(h - l for l, h in zip(box_lo, box_hi))
        missing = full - _volume_in(meshes[b.side.path], box_lo, box_hi) - _volume_in(meshes[b.shelf.path], box_lo, box_hi)
        depth, thick = case.side_t - remaining, c.across_hi - c.across_lo
        # (the joint's stations: without dog bones no relief cut counts them, and a notch is a
        # cut of its own [fuzzing, 2026-10-13])
        tenons = len(make_joint(case.joint, [c]).stations(c))
        allowed = along * tenons * thick * depth + across * c.length * depth + 8 * tenons * math.pi * r * r * depth
        if missing > allowed + 1e-3 * full:
            problems.append(f"the tenons and mortises leave {missing:.4g} mm3 of the {full:.4g} at the contact "
                            f"empty, more than {allowed:.4g}")
    return problems


def _yx(part: Board, poly: Any) -> list[tuple[float, float]]:
    """A polygon's vertices as (along the board's other axis, y)."""
    i = 0 if part.u_axis == "y" else 1
    return [(q[1 - i], q[i]) for q in poly.exterior.coords]



# -- one layout of many cases (the Fusion batch check) --------------------------------------------

JointCase = PairCase | CornerCase | CrossCase | FrameCase


def joint_cases() -> st.SearchStrategy[JointCase]:
    return st.one_of(pair_cases(), corner_cases(), cross_cases(), frame_cases())


def check(case: JointCase) -> list[str]:
    """What is wrong with the case, whichever kind it is."""
    if isinstance(case, PairCase):
        return run_pair(case)
    if isinstance(case, CornerCase):
        return run_corner(case)
    if isinstance(case, CrossCase):
        return run_cross(case)
    return run_frame(case)


def apply(case: JointCase, name: str) -> None:
    """Builds the case's boards in a module `name` and joins them, without
    the checks (`fusion_batch.py` builds many into one layout); LangError
    when the language refuses it."""
    if isinstance(case, PairCase):
        b = build(case, name)
        first = _join(b, case.joint, case.from_side)
        if case.after is not None:
            _join(b, case.after, not case.from_side, first)
    elif isinstance(case, CornerCase):
        _join_with(build_corner(case, name), _box(case), case.from_side)
    elif isinstance(case, CrossCase):
        b = build_cross(case, name)
        b.shelf.join(*[x for x in (b.side, b.other) if x is not None], using=_lap(case, b.shelf))
    else:
        fr = build_frame(case, name)
        joint = groove(case.depth, clearance=case.clearance, chamfer=case.chamfer, dogbones=case.dogbones,
                       tool=case.tool, relief=case.relief)
        if case.one_join and case.from_floor:
            fr.floor.join(*[fr.boards[k] for k in case.into], using=joint)
        else:
            for k in case.into:
                if case.from_floor:
                    fr.floor.join(fr.boards[k], using=joint)
                else:
                    fr.boards[k].join(fr.floor, using=joint)
