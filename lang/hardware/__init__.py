"""Hardware: bought parts with their own rules (see DESIGN.md, Joints and
hardware). A hardware object knows what it dictates about the parts around
it and what it does to them when mounted; `scope.mount(hardware, ...)`
hands it the scope.

So far: drawer slides (`slides`)."""
