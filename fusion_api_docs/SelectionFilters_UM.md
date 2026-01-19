# Selection Filters

When using the API to have the user select an entity you can specify which type(s) of entities are valid to be selected. For example, when using the [selectEntity](UserInterface_selectEntity.md) method of the UserInterface object the second argument is the selection filter. Also when performing selections using in a custom command using the [SelectionCommandInput](SelectionCommandInput.md) object you can define a filter to specify which type(s) of entities are selectable. The selection filter is a string. The complete list of all valid selection filter strings are listed below.

| **Filter String** | **Description** |
|----|----|
| Bodies | Select BRepBody entities (both solid and surface). |
| SolidBodies | Select solid BRepBody entities. |
| SurfaceBodies | Select open (surface) BRepBody entities. |
| MeshBodies | Select mesh bodies. |
| Faces | Select BRepFace entities of any shape on solid and surface BRepBody objects. |
| SolidFaces | Select BRepFace entities of any shape on solid BRepBody objects. |
| SurfaceFaces | Select BRepFace entities of any shape on surface BRepBody objects. |
| PlanarFaces | Select planar BRepFace entities. |
| CylindricalFaces | Select cylindrical BRepFace entities. |
| ConicalFaces | Select conical BRepFace entities. |
| SphericalFaces | Select spherical BRepFace entities. |
| ToroidalFaces | Select toroidal BRepFace entities. |
| SplineFaces | Select spline (NURBS) BRepFace entities. |
| Edges | Select BRepEdge entities of any shape. |
| LinearEdges | Select linear BRepEdge entities. |
| CircularEdges | Select circular BRepEdge (circles and arcs) entities. |
| EllipticalEdges | Select elliptical BRepEdge (full ellipses and elliptical arcs) entities. |
| TangentEdges | Select a BRepEdge that connects faces that are tangent along that edge. |
| NonTangentEdges | Select a BRepEdge that connects faces that are not tangent along that edge. |
| Vertices | Select BRepVertex entities. |
| RootComponents | Select root Component objects. |
| Occurrences | Select Occurrence objects. |
| Sketches | Select Sketch objects. |
| SketchConstraints | Selects sketch geometric and dimensions constraints. |
| Profiles | Select profiles. |
| Texts | Select sketch text. |
| SketchCurves | Select any shape of sketch entity. |
| SketchLines | Select SketchLine entities. |
| SketchCircles | Select SketchCircle entities. |
| SketchPoints | Select SketchPoint entities. |
| ConstructionPoints | Select ConstructionPoint entities. |
| ConstructionLines | Select ConstructionLine entities. |
| ConstructionPlanes | Select ConstructionPlane entities. |
| Features | Select any type of feature. |
| Canvases | Select canvases. |
| Decals | Select decals. |
| JointOrigins | Select joint origins. |
| Joints | Select joints. |
