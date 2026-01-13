# Addins for Autodesk Fusion 360

This code is in alpha state and there are no guarantees that this will work correctly for your use case.
Furthermore, updates to this code might break existing usages of the addins.

## Addins

- **Lamello**

  This places the holes for Lamello Clamex and Cabineo connectors.
- **Sheet Good Tenons**

  Creates mortise and tenon connections between sheet good boards and also (optionally) places the holes for screw, Clamex or Cabineo connectors in one go.
- **Pattern Cutouts**

  This is a collection of differently shaped pattern cutouts, e.g. triangles, rhombuses etc. The cutouts take existing inner features of the selected faces into account.

  The Froli pattern computes the best froli grid for a given rectangular surface and places cutouts accordingly.
- **Concealed Hinge**

  This places holes for concealed hinges in the door and carcass boards. Currently there's just one type of hinge implemented (Blum cliptop 110 for thin doors).
- **Door Latch**

  Places holes for door latches in the door and carcass boards. Currently this supports Everlocks and the small 44mm pull locks.
- **Dog Bones**

  Creates dog bones for inner corners based on the tool diameter. Specific edges or faces can be selected.
- **Heal Sketch Lines**

  Connects sketch curves that should be connected but are not quite. This often happens when projecting or intersecting complex geometry from e.g. a vehicle model, so that the projected curves do not form a closed profile. This addin automatically heals these curves by placing coincident constraints for end points within a tolerance.

## Installation

Just place the addins you want to use in your Fusion Addin directory. On the mac this is `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns`.

Then go Fusion's Addin panel:

![](img/doc1.png)

In there you can run the addin by switching on the run toggle. Optionally, you can enable the run-on-startup checkbox, so that you don't have to repeat this process each time you launch Fusion.

![](img/doc2.png)

## Development

To work on the addins, make sure you have VS Code installed, right-click on the plugin's name in Fusion's addin panel and choose "Edit in code editor".

![](img/doc3.png)

## License

GNU General Public License v3.0 or later

See [COPYING](COPYING) to see the full text.

## Attributions

- Lock icon by karl from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Hinage icon by Ruslan Dezign from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Triangular pattern icon by Made x Made from [Noun Project](https://thenounproject.com/browse/icons/term/lock/) (CC BY 3.0)
- Dog bone icon by shashank singh from <a href="https://thenounproject.com/browse/icons/term/dog-bone/">Noun Project</a> (CC BY 3.0)