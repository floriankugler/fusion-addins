# BRepEdges Object

Derived from: [Base](Base.md) Object  

## Description

BRepEdge collection.

## Methods

| Name | Description |
|----|----|
| [classType](BRepEdges_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepEdges_item.md) | Function that returns the specified edge using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepEdges_count.md) | The number of edges in the collection. |
| [isValid](BRepEdges_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepEdges_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepBody.concaveEdges](BRepBody_concaveEdges.md), [BRepBody.convexEdges](BRepBody_convexEdges.md), [BRepBody.edges](BRepBody_edges.md), [BRepFace.edges](BRepFace_edges.md), [BRepLoop.edges](BRepLoop_edges.md), [BRepLump.edges](BRepLump_edges.md), [BRepShell.edges](BRepShell_edges.md), [BRepVertex.edges](BRepVertex_edges.md), [BRepWire.edges](BRepWire_edges.md)

## Samples

| Name | Description |
|----|----|
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version August 2014  

