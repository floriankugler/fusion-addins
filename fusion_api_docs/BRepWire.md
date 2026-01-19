# BRepWire Object

Derived from: [Base](Base.md) Object  

## Description

Represents a single B-Rep wire body. A wire body consists of one or more edges and their vertices.

## Methods

| Name | Description |
|----|----|
| [classType](BRepWire_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](BRepWire_createForAssemblyContext.md) | Returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [offsetPlanarWire](BRepWire_offsetPlanarWire.md) | Method that computes the offset for a planar wire. A BRepBody containing the resulting BRepWire object(s) is returned. It's possible that the offset result of a single wire can result in multiple wires. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](BRepWire_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this BRepFace object is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly. but is already the native object. |
| [coEdges](BRepWire_coEdges.md) | Returns the co-edges associated with this wire body. The co-edges record the connections between the edges in the wire body. |
| [edges](BRepWire_edges.md) | Returns the B-Rep edges associated with this wire body. |
| [isPlanar](BRepWire_isPlanar.md) | Indicates if this entities making up this wire body are planar and all lie on the same plane. |
| [isValid](BRepWire_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [nativeObject](BRepWire_nativeObject.md) | The NativeObject is the object outside the context of an assembly. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](BRepWire_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](BRepWire_parent.md) | Returns the parent BRepBody object that contains this wire. |
| [vertices](BRepWire_vertices.md) | Returns the B-Rep vertices associated with this wire body. |

## Accessed From

[BRepShell.wire](BRepShell_wire.md), [BRepWire.createForAssemblyContext](BRepWire_createForAssemblyContext.md), [BRepWire.nativeObject](BRepWire_nativeObject.md), [BRepWires.item](BRepWires_item.md)

## Version

Introduced in version December 2017  

