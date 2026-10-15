"""What the type checker must report in a build file.

Pyright checks this file with the rest (`.venv/bin/pyright`); pytest does
not run it. Each line marked `# type: ignore` must have an error: if a
change to the language made it pass, pyright reports the comment as
unnecessary, and the check fails.
"""
# pyright: reportUnnecessaryTypeIgnoreComment=true
from lang import *
from lang.std import carcass, drawer_box

ply15 = sheet_material("birch", t=15)


def operations() -> None:
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        side = board("side", ply15).on(m.left)
        _ = side.toekick.top                                                 # a named operation: fine
        side.pocket(rect(depth=50, height=50), at=side.inner.center)          # type: ignore  # no depth
        side.hole(5, side.inner.center)                                       # type: ignore  # no depth
        side.pocket(rect(depth=50, height=50), side.inner.center, 5)          # type: ignore  # depth by position
        side.pocket(rect(depth=50, height=50), depth=to(side.outer, leave=3))  # fine
        side.pocket(rect(depth=50, height=50), depth=to(side.outer, -3))      # type: ignore  # leave= by keyword
        side.hole(5, depth=to("outer", 3))                                    # type: ignore  # leave= by keyword
        side.hoel(d=5, at=side.inner.center, depth=10)                        # type: ignore  # a misspelt method
        side.fillet(side.front.bottom, r=5)                                   # type: ignore  # radius=, not r=
        a, b = side.inner.front(40).bottom(100), side.inner.front(40).bottom(300)
        side.slot(8, a, b, depth=10)                                          # two end centres: fine
        side.slot(8, at=a, centers=52, along="height", depth=10)              # a centre: fine
        side.slot(8, at=a, centers=52, along=m.top, depth=10)                 # along a side: fine
        side.slot(8, a, depth=10)                                             # type: ignore  # one anchor
        side.slot(8, a, b, at=a, depth=10)                                    # type: ignore  # both forms
        side.slot(8, at=a, centers=52, depth=10)                              # type: ignore  # no along=
        side.slot(8, at=a, length=60, along="height", depth=10)               # type: ignore  # centers=, not length=
        side.slot(8, at=a, centers=52, along="heigth", depth=10)              # type: ignore  # a misspelt extent
        side.slot(width=8, at=a, centers=52, along="height", depth=10)        # type: ignore  # width by position
        side.slot(8, a, b)                                                    # type: ignore  # no depth



def slats() -> None:
    oak = slat_material("oak")
    with module("s", Box.from_size(width=600, depth=400, height=700)) as m:
        cleat = slat("cleat", oak, section=(20, 40)).on(m.left).edge_on(m.top)   # fine
        cleat.center(m.center("depth"))                                       # fine (refused at run time)
        slat("rail", oak, (20, 40))                                           # type: ignore  # section= by keyword
        slat("rail", ply15, section=(20, 40))                                 # type: ignore  # a sheet material
        slat("rail", oak, section=20)                                         # type: ignore  # two sizes
        slat_material("oak", 20, 40)                                          # type: ignore  # only a species
        board("top", oak)                                                     # type: ignore  # a slat material
        shelf = board("shelf", ply15).on(m.bottom)
        shelf.lip(shelf.front, 10, oak)                                       # fine
        shelf.lip([shelf.left, shelf.right], 0.5, oak)                        # a list: fine
        shelf.lip(shelf.back, 10, ply15)                                      # type: ignore  # lips are solid wood
        shelf.lip(shelf.back, t=10)                                           # type: ignore  # no material
        shelf.edge_on(m.left)                                                 # type: ignore  # a board has no edge_on


def references() -> None:
    """A side or a face plus or minus a number is refused: `into()` and
    `gap()` say which way (syntax.md item 1)."""
    with module("r", Box.from_size(width=600, depth=400, height=700)) as m:
        shelf = board("shelf", ply15).on(m.bottom)
        _ = m.bottom.into(60), shelf.top.gap(5), m.bottom.position + 60, shelf.top.position - 5     # fine
        _ = (m.bottom + shelf.top) / 2, m.top - m.bottom, 0.5 * m.bottom + 0.5 * shelf.top        # fine
        _ = m.bottom + 60                                                     # type: ignore  # a side has a direction
        _ = m.top - 60                                                        # type: ignore  # into() or gap()
        _ = 60 + m.bottom                                                     # type: ignore  # the number first
        _ = m.bottom.into(60) + 5                                             # type: ignore  # a moved side
        _ = shelf.top + 5                                                     # type: ignore  # a face
        _ = shelf.top.gap(5) - 5                                              # type: ignore  # a moved face


def joints() -> None:
    top = world_frame().direction("top")
    with module("j", Box.from_size(width=600, depth=400, height=40)) as m:
        half_lap(m.top, split=m.bottom.into(10), clearance=0.2)
        half_lap(m.top, at=m.bottom.into(10))                                 # type: ignore  # split=, not at=
        half_lap(m.top, m.bottom.into(10))                                    # type: ignore  # settings by keyword
    half_lap(top, clearance=0.2, dogbones=None)
    tenons(2, width=50, dogbones=None)
    tenons(2, 50)                                                             # type: ignore  # width= by keyword
    domino("4x20", count=2, end=None)
    domino("4x20", 2)                                                         # type: ignore  # count= by keyword
    domino("4x20", at=Pos("x", 100))                                          # type: ignore  # at= takes a list
    cabineo(at=[Pos("x", 100)], surface="flush")
    screws(4, 3)                                                              # type: ignore  # count= by keyword
    box_joint(5, 2)                                                           # type: ignore  # margin= by keyword
    groove(5, (0.5, 0.5))                                                     # type: ignore  # clearance= by keyword


def shapes() -> None:
    rect(depth=50, height=50).clip(top=10, back=10)
    rect(depth=50, height=50).clip("top.back", top=10, back=10)               # type: ignore  # no strings
    rect(depth=50, height=50).clip(top=10, bak=10)                            # type: ignore  # a misspelt edge


def hardware() -> None:
    """`scope.mount(hardware, ...)` takes the hardware's own typed keywords."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        side = board("side", ply15).on(m.left)
        other = board("other", ply15).on(m.right)
        door = board("door", ply15).on(m.front)
        hinge = ConcealedHinge(count=3, end=80, pilot=(3, 3))
        m.mount(hinge, door=door, carcass=side)                                   # fine
        m.mount(hinge, door=door, carcass=side.inner)                             # a face: fine
        m.mount(hinge, dor=door, carcass=side)                                    # type: ignore  # a misspelt keyword
        m.mount(hinge, door=door)                                                 # type: ignore  # carcass= missing
        m.mount(hinge, door=side.inner, carcass=side)                             # type: ignore  # a face as the door
        m.mount(hinge, door, side)                                                # type: ignore  # keywords only
        ConcealedHinge(margin=60)                                                 # type: ignore  # end=, not margin=
        ConcealedHinge(predrill=(3, 3))                                           # type: ignore  # pilot=
        slide = DrawerSlide("Dynapro 40", nl=450, pilot=(2, 4))
        m.mount(slide, sides=(side, other), front=door.back)                      # fine
        m.mount(slide, sides=[side, other], front=door.back)                      # a list: fine
        m.mount(slide, sides=side, front=door.back)                               # type: ignore  # one side
        m.mount(slide, sides=(side, other))                                       # type: ignore  # front= missing
        DrawerSlide("Dynapro 41", nl=450)                                         # type: ignore  # no such model
        DrawerSlide("Dynapro 40", 450, 4)                                         # type: ignore  # holes= keyword-only
        latch = DoorLatch("Pull Lock 44", count=2)
        m.mount(latch, door=door, carcass=side.inner)                             # fine
        m.mount(latch, door=door, carcass=side, count=2)                          # type: ignore  # count is latch's
        DoorLatch("Pull Lock 44", 2)                                              # type: ignore  # count keyword-only
        DoorLatch("Pull Lock 44", predrill=(3, 3))                                # type: ignore  # pilot=
        HatchHinge("Free space 1.11", opening=90)                                 # fine
        m.mount(HatchHinge("Free space 1.11"), hatch=door, sides=(side, other), top=m.top)    # fine
        m.mount(HatchHinge("Free space 1.11"), hatch=door, side=side, top=m.top)  # type: ignore  # sides=
        SlidingBracket("Pacofix PF-L", count=3, frame_hole="euro")                # fine
        m.mount(SlidingBracket(), panel=door, frame=[side, other.inner])          # fine
        m.mount(SlidingBracket(), panel=door, frame=[side], at=[m.bottom])        # type: ignore  # at= is the bracket's
        SlidingBracket(frame_hole="m4")                                           # type: ignore  # no such hole
        BallCatch(count=4, end=40)                                                # fine
        BallCatch("GN 450", 4)                                                    # type: ignore  # count keyword-only


def hardware_factories() -> None:
    """The factories take their classes' parameters, checked the same."""
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        side = board("side", ply15).on(m.left)
        other = board("other", ply15).on(m.right)
        door = board("door", ply15).on(m.front)
        made: ConcealedHinge = hinge(count=3, end=80, pilot=(3, 3))               # its class: fine
        m.mount(made, door=door, carcass=side)                                    # fine
        m.mount(hinge(), dor=door, carcass=side)                                  # type: ignore  # a misspelt keyword
        hinge(margin=60)                                                          # type: ignore  # end=, not margin=
        hinge(predrill=(3, 3))                                                    # type: ignore  # pilot=
        hinge("Blum CLIP top 110 Thin +2")                                        # type: ignore  # no such model
        hinge("Blum CLIP top 110 Thin +0", 3)                                     # type: ignore  # count keyword-only
        slide: DrawerSlide = drawer_slide("Dynapro 40", nl=450, pilot=(2, 4))     # fine
        m.mount(slide, sides=(side, other), front=door.back)                      # fine
        m.mount(slide, sides=side, front=door.back)                               # type: ignore  # one side
        drawer_slide("Dynapro 41", nl=450)                                        # type: ignore  # no such model
        drawer_slide("Dynapro 40", 450, 4)                                        # type: ignore  # holes= keyword-only
        drawer_slide("Dynapro 40", nl=450, hole=4)                                # type: ignore  # holes=, not hole=
        lock: DoorLatch = latch("Pull Lock 44", count=2)                          # fine
        m.mount(lock, door=door, carcass=side, count=2)                           # type: ignore  # count is latch's
        latch("Pull Lock 44", 2)                                                  # type: ignore  # count keyword-only
        latch("Pull Lock 44", predrill=(3, 3))                                    # type: ignore  # pilot=
        latch("Pull Lock 45")                                                     # type: ignore  # no such model
        flap: HatchHinge = hatch_hinge("Free space 1.11", opening=90)             # fine
        m.mount(flap, hatch=door, sides=(side, other), top=m.top)                 # fine
        hatch_hinge("Free space 1.11", 90)                                        # type: ignore  # opening keyword-only
        hatch_hinge("Free space 1.11", opening=95)                                # type: ignore  # no such opening
        hatch_hinge("Free space 1.12")                                            # type: ignore  # no such model
        bracket: SlidingBracket = sliding_bracket("Pacofix PF-L", count=3, frame_hole="euro")  # fine
        m.mount(bracket, panel=door, frame=[side, other.inner])                   # fine
        sliding_bracket(frame_hole="m4")                                          # type: ignore  # no such hole
        sliding_bracket("Pacofix PF-L", 3)                                        # type: ignore  # count keyword-only
        sliding_bracket("Pacofix PF-X")                                           # type: ignore  # no such model
        catch: BallCatch = ball_catch(count=4, end=40)                            # fine
        ball_catch("GN 450", 4)                                                   # type: ignore  # count keyword-only
        ball_catch("GN 451")                                                      # type: ignore  # no such model
        ball_catch(count=4, ends=40)                                              # type: ignore  # end=, not ends=
        del catch


def modules() -> None:
    van = Box.from_size(width=2000, depth=1000, height=1000)
    cabinet("kitchen", van, front=van.right)
    module("floor", van)
    module("kitchen", van, front=van.right)                                  # type: ignore  # a cabinet
    cabinet("kitchen", van)                                                  # type: ignore  # no front


def std() -> None:
    """The standard library's blocks are typed like the core."""
    oak = slat_material("oak")
    ply9 = sheet_material("birch", t=9)
    box = Box.from_size(width=600, depth=400, height=700)
    with cabinet("c", box, front=box.right) as cab:
        left, right, bottom, top, back = carcass(cab, ply15, back=ply9, toekick=(60, 100))   # fine
        back.join(left, right, using=domino("4x20", count=2))                               # the back is a Board
        _ = carcass(cab, ply15).back                                                        # type: ignore  # no back without back=
        carcass(cab, ply15, ply9)                                                           # type: ignore  # back= by keyword
        carcass(cab, ply15, back_joins=domino("4x20", count=2))                             # type: ignore  # nothing to join
        carcass(cab, oak)                                                                   # type: ignore  # a slat material
        carcass(cab, ply15, front="front")                                                  # type: ignore  # a limit, not a string
        slide = drawer_slide("Dynapro 40", nl=450)
        with scope("d", cab.interior) as d:
            face = board("face", ply15).on(cab.interior.front)
            drawer_box(d, cab.interior, slide, front=face.back, height=100, material=ply15, floor=ply9,
                       corners=None, floor_joint=groove(5), carcass=[left, right])          # fine
            drawer_box(d, cab.interior, slide, front=face.back, height=100, material=ply15, floor=ply9,
                       carcass=[left, right])                                               # type: ignore  # corners= and floor_joint= are said
            drawer_box(d, cab.interior, slide, face.back, 100, ply15, ply9, None, None, [left, right])  # type: ignore  # keywords
    _ = bottom, top
