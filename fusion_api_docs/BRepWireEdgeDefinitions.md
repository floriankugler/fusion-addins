# BRepWireEdgeDefinitions Object

Derived from: [Base](Base.md) Object  

## Description

A collection of BRepWireEdgeDefinition objects. Using this collection you can create new BRepWireDefinition objects to full define a wire body.

## Methods

| Name | Description |
|----|----|
| [add](BRepWireEdgeDefinitions_add.md) | Creates a new BRepWireEdgeDefinition object associated with the parent BRepWireDefinition object. |
| [classType](BRepWireEdgeDefinitions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepWireEdgeDefinitions_item.md) | Function that returns the specified BRepWireEdgeDefinition object using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepWireEdgeDefinitions_count.md) | The number of B-Rep wire edge definition objects in the collection. |
| [isValid](BRepWireEdgeDefinitions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepWireEdgeDefinitions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepWireDefinition.wireEdgeDefinitions](BRepWireDefinition_wireEdgeDefinitions.md)

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

