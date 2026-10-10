"""The drawer cabinet from DESIGN.md, as far as phase 1 reaches: boards and
their placement, cuts, pockets and holes. No joints and no hardware yet, so
the slide is a stand-in with the numbers a real slide module will own."""
from lang import *

ply15 = material("birch", t=15, sheet=(2500, 1250))
ply12 = material("birch", t=12, sheet=(2500, 1250))
ply9 = material("birch", t=9, sheet=(2500, 1250))
GAP = 3  # between fronts


class StandInSlide:
    """Until the drawer-slide module exists: a runner needing 13 mm per side
    and lifting the drawer floor 10 mm."""
    side_clearance = 13
    recess = 10

    def box_space(self, bay: Box, behind: Board, height: float) -> Box:
        inner = bay.with_side("front", behind.back.value)
        return inner.shrunk(left=self.side_clearance, right=self.side_clearance).with_side(
            "top", inner.bottom.value + height)


def drawer_cabinet(name: str, box: Box, n: int, slide: StandInSlide) -> Scope:
    with module(name, box) as cab:
        left = board("left", ply15).on(cab.left)
        right = board("right", ply15).on(cab.right)
        bottom = board("bottom", ply15).on(cab.bottom).between(left, right)
        top = board("top", ply15).on(cab.top).between(left, right)
        board("back", ply9).on(cab.back).between(left, right, bottom, top)

        # toe kick notch in both sides, named so its faces can be referenced
        for side in (left, right):
            side.cut(rect(60, 100), at="bottom.front", name="toekick")

        # shelf-pin holes on the inner faces, lined up on both sides
        for side in (left, right):
            for z in spread(bottom.top + 100, top.bottom - 100, pitch=32):
                side.hole(d=5, depth=10, face="inner", at=("front", 37, z))

        for i, bay in enumerate(cab.interior.split("z", n), 1):
            drawer(f"drawer{i}", bay, slide)

        cab.export("worktop", top.top)   # for whatever stands on the cabinet
        check(no_interference, fits_sheet)
    return cab


def drawer(name: str, bay: Box, slide: StandInSlide) -> Scope:
    with scope(name, bay) as d:
        board("face", ply15).on(bay.front).inset(GAP / 2)
        box = slide.box_space(bay, behind=d.face, height=bay.height - 30)

        l = board("left", ply12).on(box.left).between(box.front, box.back, box.bottom, box.top)
        r = board("right", ply12).on(box.right).between(box.front, box.back, box.bottom, box.top)
        f = board("front", ply12).on(box.front).between(l, r, box.bottom, box.top)
        k = board("back", ply12).on(box.back).between(l, r, box.bottom, box.top)
        # the floor reaches 5 mm into the sides
        floor = (board("floor", ply9)
                 .on(box.bottom + slide.recess)
                 .between(l.into(5), r.into(5), f, k))
        # the grooves: what the floor occupies in each side, with 0.5 mm of
        # room above the floor and beyond its edges
        room = floor.box().grown(top=0.5, left=0.5, right=0.5)
        for side in (l, r):
            side.cut(room, name="floor_groove")
    return d


cabinet = drawer_cabinet("drawercab", Box.from_size(width=600, depth=500, height=720), 3, StandInSlide())
