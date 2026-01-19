# BRepLump Object

Derived from: [Base](Base.md) Object  

## Description

Represents an entirely connected set of entities. A BRepBody consists of BRepLumps.

## Methods

| Name | Description |
|----|----|
| [classType](BRepLump_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](BRepLump_createForAssemblyContext.md) | Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [pointContainment](BRepLump_pointContainment.md) | Determines the relationship of the input point with respect to this lump. |

## Properties

| Name | Description |
| --- | --- |
| [area](BRepLump_area.md) | Returns the area in cm ^ 2. |
| [assemblyContext](BRepLump_assemblyContext.md) | Returns the assembly context that is directly referencing this object in an assembly. This is only valid in the case where this BRepLump object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object. |
| [body](BRepLump_body.md) | Returns the immediate owner BRepBody of the lump |
| [boundingBox](BRepLump_boundingBox.md) | Returns the bounding box of the lump |
| [edges](BRepLump_edges.md) | Returns the BRepEdges owned by the lump |
| [entityToken](BRepLump_entityToken.md) | Returns a token for the BRepLump object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same lump. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. This is only valid for lump that exist in the design, (the isTemporary property is false). |
| [faces](BRepLump_faces.md) | Returns the BRepFaces owned by the lump |
| [isClosed](BRepLump_isClosed.md) | Returns true of the lump is closed |
| [isValid](BRepLump_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [meshManager](BRepLump_meshManager.md) | Returns the mesh manager object for this lump. |
| [nativeObject](BRepLump_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](BRepLump_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [shells](BRepLump_shells.md) | Returns the BRepShells owned by the lump |
| [vertices](BRepLump_vertices.md) | Returns the BRepVertices owned by the lump |
| [volume](BRepLump_volume.md) | Returns the volume in cm ^ 3. Returns 0 in the case the lump is not solid. |

## Accessed From

[BRepLump.createForAssemblyContext](BRepLump_createForAssemblyContext.md), [BRepLump.nativeObject](BRepLump_nativeObject.md), [BRepLumps.item](BRepLumps_item.md), [BRepShell.lump](BRepShell_lump.md)

## Version

Introduced in version August 2014  

