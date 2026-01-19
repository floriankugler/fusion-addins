# BRepShell Object

Derived from: [Base](Base.md) Object  

## Description

Represents an entirely connected set of BRepFaces. A BRepLump may contain multiple BRepShells.

## Methods

| Name | Description |
|----|----|
| [classType](BRepShell_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](BRepShell_createForAssemblyContext.md) | Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [pointContainment](BRepShell_pointContainment.md) | Determines the relationship of the input point with respect to this shell. |

## Properties

| Name | Description |
| --- | --- |
| [area](BRepShell_area.md) | Returns the area in cm ^ 2. |
| [assemblyContext](BRepShell_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this BRepShell object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object. |
| [body](BRepShell_body.md) | Returns the parent body of the shell. |
| [boundingBox](BRepShell_boundingBox.md) | Returns the bounding box of this shell |
| [edges](BRepShell_edges.md) | returns the BRepEdges owned by this shell |
| [entityToken](BRepShell_entityToken.md) | Returns a token for the BRepShell object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same shell. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. This is only valid for shells that exist in the design, (the isTemporary property is false). |
| [faces](BRepShell_faces.md) | Returns the BRepFaces directly owned by this shell |
| [isClosed](BRepShell_isClosed.md) | Returns true if this shell is closed |
| [isValid](BRepShell_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVoid](BRepShell_isVoid.md) | Returns true if the faces of this shell bound a void or an empty space within an outer shell. |
| [lump](BRepShell_lump.md) | Returns the parent lump of this shell. |
| [meshManager](BRepShell_meshManager.md) | Returns the mesh manager object for this shell. |
| [nativeObject](BRepShell_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](BRepShell_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [vertices](BRepShell_vertices.md) | Returns the BRepVertices owned by this shell |
| [volume](BRepShell_volume.md) | Returns the volume in cm ^ 3. Returns 0 in the case the shell is not solid. |
| [wire](BRepShell_wire.md) | Returns the wire body, if any, that exists in this shell. Returns null if the shell doesn't have a wire body. |

## Accessed From

[BRepEdge.shell](BRepEdge_shell.md), [BRepFace.shell](BRepFace_shell.md), [BRepShell.createForAssemblyContext](BRepShell_createForAssemblyContext.md), [BRepShell.nativeObject](BRepShell_nativeObject.md), [BRepShells.item](BRepShells_item.md), [BRepVertex.shell](BRepVertex_shell.md)

## Version

Introduced in version August 2014  

