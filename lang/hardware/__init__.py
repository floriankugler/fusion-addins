"""Hardware: bought parts with their own rules (see DESIGN.md, Joints and
hardware). A hardware object knows what it dictates about the parts around
it and what it does to them when mounted; `scope.mount(hardware, ...)`
hands it the scope.

So far: drawer slides (`slides`), concealed hinges (`hinges`), lift-up
hatch hinges (`hatch_hinges`), ball catches for inspection hatches
(`ball_catches`) and door latches (`latches`). Each places its bought part
as boxes (`scope.place_hardware`) from one table of sizes measured from
the makers' CAD models and drawings, kept apart from the drilling data
in `lib/`."""
