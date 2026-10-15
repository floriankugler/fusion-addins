"""What the type checker must report in a build file.

Pyright checks this file with the rest (`.venv/bin/pyright`); pytest does
not run it. Each line marked `# type: ignore` must have an error: if a
change to the language made it pass, pyright reports the comment as
unnecessary, and the check fails.
"""
# pyright: reportUnnecessaryTypeIgnoreComment=true
from lang import *

ply15 = sheet_material("birch", t=15)


def operations() -> None:
    with module("m", Box.from_size(width=600, depth=400, height=700)) as m:
        side = board("side", ply15).on(m.left)
        _ = side.toekick.top                                                 # a named operation: fine
        side.pocket(rect(depth=50, height=50), at=side.inner.center)          # type: ignore  # no depth
        side.hole(5, side.inner.center)                                       # type: ignore  # no depth
        side.pocket(rect(depth=50, height=50), side.inner.center, 5)          # type: ignore  # depth by position
        side.hoel(d=5, at=side.inner.center, depth=10)                        # type: ignore  # a misspelt method
        side.fillet(side.front.bottom, r=5)                                   # type: ignore  # radius=, not r=
        a, b = side.inner.front(40).bottom(100), side.inner.front(40).bottom(300)
        side.slot(8, a, b, depth=10)                                          # two end centres: fine
        side.slot(8, at=a, centres=52, along="height", depth=10)              # a centre: fine
        side.slot(8, at=a, centres=52, along=m.top, depth=10)                 # along a side: fine
        side.slot(8, a, depth=10)                                             # type: ignore  # one anchor
        side.slot(8, a, b, at=a, depth=10)                                    # type: ignore  # both forms
        side.slot(8, at=a, centres=52, depth=10)                              # type: ignore  # no along=
        side.slot(8, at=a, length=60, along="height", depth=10)               # type: ignore  # centres=, not length=
        side.slot(8, at=a, centres=52, along="heigth", depth=10)              # type: ignore  # a misspelt extent
        side.slot(width=8, at=a, centres=52, along="height", depth=10)        # type: ignore  # width by position
        side.slot(8, a, b)                                                    # type: ignore  # no depth
        side.machine(side.inner)                                              # a face: fine
        side.machine("inside")                                                # type: ignore  # inner or outer



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


def joints() -> None:
    top = world_frame().direction("top")
    with module("j", Box.from_size(width=600, depth=400, height=40)) as m:
        half_lap(m.top, split=m.bottom + 10, clearance=0.2)
        half_lap(m.top, at=m.bottom + 10)                                     # type: ignore  # split=, not at=
        half_lap(m.top, m.bottom + 10)                                        # type: ignore  # settings by keyword
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


def modules() -> None:
    van = Box.from_size(width=2000, depth=1000, height=1000)
    cabinet("kitchen", van, front=van.right)
    module("floor", van)
    module("kitchen", van, front=van.right)                                  # type: ignore  # a cabinet
    cabinet("kitchen", van)                                                  # type: ignore  # no front
