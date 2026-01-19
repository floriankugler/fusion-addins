# OperationStrategyTypes Enumerator

## Description

The valid options for the Strategy Type of an operation.  

## Methods

| Name | Value | Description |
|----|----|----|
| AdaptiveClearing | 10 | A 3D roughing strategy for clearing large quantities of material effectively. |
| AdaptiveClearing2D | 0 | A 2D strategy that creates a roughing operation that uses a more optimized toolpath that avoids abrupt direction changes. |
| Bore | 7 | A 2D strategy for milling cylindrical pockets and islands by selecting the cylindrical geometry directly. |
| Chamfer2D | 36 | A 2D machining strategy that machines along contours creating a chamfered surface. |
| Circular | 8 | A 2D strategy for milling cylindrical pockets and islands. |
| Contour | 13 | A 3D strategy for finishing steep walls, but can be used for semi-finish and finish machining on the more vertical areas of a part. |
| Contour2D | 3 | A 2D strategy that creates toolpaths based on a 2D contour. Contours can be open or closed and can be on different Z-levels, but each contour is flat (2D). |
| Drilling | 22 | A strategy that supports a wide range of drilling, tapping and hole making operations such as counterbores and countersinks. |
| Engrave | 9 | A 2D strategy that machines along contours with V-shaped chamfered walls. |
| Face | 2 | A 2D strategy that produces quick part facing to prepare raw stock for machining. |
| Flow | 33 | A 3D finishing strategy which follows the isocurves of a surface to machine parts with curved surfaces. Flow is a 3-Axis toolpath by default but can be used in multi-axis modes. |
| Flow2 | 34 | A 3D finishing strategy which follows the isocurves of a surface to machine parts with curved surfaces. Flow is a 3-Axis toolpath by default but can be used in multi-axis modes. |
| Horizontal | 15 | A 3D strategy that automatically detects all the flat areas of the part and clears them with an offsetting path. |
| Jet2D | 23 | A strategy that creates a 2D toolpath for waterjet, laser, and plasma cutting processes. |
| ManualInspection | 43 | Manual inspection. |
| ManualMeasure | 48 | Recorded results of a manual inspection. |
| Morph | 37 | A 3D finishing strategy for machining shallow areas between selected contours with a consistent cutting direction. |
| MorphedSpiral | 20 | A 3D strategy similar to Spiral except that this operation generates the spiral from the selected boundary as opposed to Spiral which trims the generated passes to the machining boundary. |
| MultiAxisContour | 38 | A multi-axis strategy for machining with the tip of the tool along a given contact curve. |
| MultiAxisMorph | 39 | A multi-axis strategy for machining shallow areas between selected contours with a consistent cutting direction. |
| Parallel | 12 | A 3D finishing strategy. The passes are parallel in the XY-plane and follow the surface in the Z-direction. |
| PartAlignment | 46 | Part alignment. |
| PathMeasure | 47 | A surface inspection measurement with a results folder. |
| Pencil | 16 | A 3D strategy that creates toolpaths along internal corners and fillets with small radii, removing material that no other tool can reach. |
| Pocket2D | 1 | A 2D strategy that creates a roughing operation that uses toolpaths parallel to selected geometry. |
| PocketClearing | 11 | A 3D conventional roughing strategy for clearing large quantities of material effectively. |
| ProbeGeometry | 45 | Probe Geometry operation |
| ProbeWCS | 44 | Probe WCS operation |
| Projection | 21 | A finishing strategy that allows you to machine along contours with the center of the tool. The provided contours are automatically projected onto the surface, so they do not have to actually lie on the surface. |
| Radial | 19 | A 3D strategy similar to Spiral machining. This operation also starts from a center point, providing the ability to machine radial parts. It also provides the option to stop short of the center of the radial passes, where they become very dense. |
| Ramp | 14 | A 3D finishing strategy intended for steep areas similar to the contour strategy. However, this strategy ramps down walls rather than machining them with a constant Z, as contour does. |
| RestFinishing | 40 | A finishing operation to machine any remaining stock left from previous operations. |
| RotaryFinishing | 35 | A multi-axis machining strategy that lets you machine along and around a rotating axis. Rotary Finishing can be used for parts that are machined most efficiently when utilizing the 4th Machine Axis. |
| Scallop | 17 | A 3D strategy that creates passes at a constant distance from one another by offsetting them inwards along the surface. The passes follow sloping and vertical walls to maintain the stepover. |
| Slot | 4 | A 2D strategy that mills a slot by following the center line of the slot. |
| Spiral | 18 | A 3D strategy that creates a spiral toolpath from a given center point, generating a constant contact as it machines within a given boundary. |
| SteepAndShallow | 32 | A 3D finishing strategy that uses Contour passes for steep areas and Parallel or Scallop passes for shallow areas. |
| SurfaceInspection | 42 | A strategy for the inspection of geometry using probe. |
| Swarf | 41 | A multi-axis strategy for machining with the side of the tool. |
| Thread | 6 | A 2D strategy for thread milling cylindrical pockets and islands. |
| Trace | 5 | A 2D strategy that machines along contours with varying Z values and with, or without, left and right side compensation. |
| TurningChamfer | 24 | The turning chamfer strategy is used for chamfering sharp corners that have not been chamfered in the design. |
| TurningFace | 25 | The face strategy is used for machining the front side of the part. |
| TurningGroove | 26 | The turning groove strategy is used for grooving at selected positions only. This can for instance be used to make a groove on the backside before threading. |
| TurningPart | 27 | This strategy is used for cutting off the part once the part has been fully machined or for machining it on another spindle. |
| TurningProfile | 28 | The turning profile strategy is used for both roughing and finishing of the part using general turning tools. |
| TurningProfileGroove | 29 | The turning groove strategy is used for both roughing and finishing of the part using groove tools. |
| TurningStockTransfer | 30 | The turning stock transfer strategy is intended for automatic stock transfer between the two spindles. No toolpath is associated with this strategy. The post is responsible for outputting the desired NC code. |
| TurningThread | 31 | This strategy is used for turning threads. Both cylindrical and conical threads are supported. The CNC control must have built-in support for synchronizing the spindle and feed. |

## Version

Introduced in version January 2016  

