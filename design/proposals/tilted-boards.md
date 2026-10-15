# Tilted boards

Status: added by Florian 2026-10-14, worked out by Claude the same day;
nothing built. Only the points marked [Florian] are his. The spellings are
working titles, to be settled in a detailed plan before implementing
[Florian]. Comes before miters at angles other than 90 degrees
(`miters.md`); fitted ends need bevels (`bevels.md`).

Boards that lie in no plane of their scope's frame, turned about one of its
axes [Florian: usually about one axis]. Florian's case is an overhead cabinet
whose front slopes, so the cabinet is shallower at the bottom: the sides are
cut to the slope and the front sits between their sloped edges.

Today every board lies in a plane of the world axes, at every level: a
position is a coordinate on one axis, the layout names each part's axes by
world axis, contacts and crossings run along world axes, and a tilted master
plane is an error where it is used as a position.

Proposed:

- A tilted plane is a reference: a master `Plane` (origin and normal,
  already in the snapshot), or the face of a cut at an angle.
  `side.trim(a, b, name=)` is such a cut, a new operation: a straight cut
  through two anchors on a big face, taking off the side the board's centre
  is not on. It is `clip()` for a placed board, its ends given by anchors.
- `.on()` a tilted face or plane gives the board that plane, and `toward=`
  says which way the thickness goes, as on a bare plane. `.between()` takes
  limits on the axis the board shares with its scope (the axis it is turned
  about) as now. On the tilted axis it takes planes and faces: the board ends
  where its material meets them over its whole thickness, the tighter of its
  two faces, as a contour in a perpendicular plane limits a board now. Its
  ends stay square, inside the limits; `bevel(end, to=limit)` fits an end to
  its limit.
- A tilted board's faces are named by the nearest direction, the rule
  already proposed for hand-modeled bodies (`copy-path.md`), so the sloped
  front keeps `front`, `back`, `top` and the rest. A tilt of 45 degrees is an
  error that names the part; `inner` and `outer` work as before.
- Underneath, the layout carries a rotation per part instead of axis names,
  which is a new layout version. The plan and the mesher place the outline
  with it; the emitter already builds bodies from world geometry.
- A contact may run at an angle across the board that is met face-on, so a
  tilted board standing edge-on on a square one (the front's ends on the
  sides) joins as now, with its connectors turned in the side's face, which
  the machine cuts as easily as square ones. A board that meets another at
  an angle (the top's front edge against the sloped front) is no contact. It
  is fixed by hand (screws, glue) or mitred.
- `no_interference` checks pairs with a tilted part through the preview's
  meshes. Hardware on tilted parts comes later.
- A part turned about two axes stays out of scope and is hand-modeled.

```python
left = board("left", ply15).on(cab.left).between(cab.top, cab.bottom, cab.back, cab.front)
left.trim(left.inner.front.top, left.inner.front(100).bottom, name="slope")  # 100 shallower at the bottom
right = board("right", ply15).on(cab.right).between(cab.top, cab.bottom, cab.back, cab.front)
right.trim(right.inner.front.top, right.inner.front(100).bottom, name="slope")
front = (board("front", ply15)
         .on(left.slope, toward=cab.back)   # flush with the sloped edges, between the sides
         .between(left, right, top, bottom))
front.join(left, right, using=domino("5x30", count=2))  # contacts along the slope
```
