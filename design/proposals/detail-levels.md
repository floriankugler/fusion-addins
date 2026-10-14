# Detail levels

Status: the workflow is decided, the mechanism proposed; nothing built.

Florian models incrementally: rough shapes first, then holes, chamfers and
the choice of connectors. The language does not replicate that as separate
stages. The module is written once, boards first and relations after, and
detail is added below, not by editing the boards. [decided as a workflow]

- In Fusion the stages protect work from invalidation: a hole pattern dies
  when its face moves. In the language a hole is a relation to a named face,
  a joint a relation to a contact, a slide pattern follows the bay, so
  details survive shape changes and there is no cost to adding them early or
  late.
- Details have homes. Joints and hardware go into relation lines after the
  boards. One-offs go inline next to the board they concern. A rough module
  is the boards and their placement; a finished module is the same file plus
  join and mount lines.
- Details that drive the rough shape are chosen early as families with
  defaults: the slide family decides drawer box width and floor recess, the
  connector family and front gap decide the carcass. They are stated once in
  the build and refined to exact models later, in one place.
- A **detail level** is a compile and preview switch: `rough` shows outlines
  and placement only; `full` shows joints, holes, chamfers and hardware. The
  layout step skips the operations below the requested level. A level is a
  filter on operations and never a second code path, so the rough preview
  cannot lie about the shape. Tenons change the outline, so in rough mode a
  board shows its plain outline, which is what one draws by hand at that
  stage.

Open: two levels or three, and whether chamfers belong to `full` or to a
middle level with holes but without joints.
