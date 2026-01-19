# BRepCoEdgeDefinitions Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the BRepCoEdgeDefinition objects associated with the parent BRepLoopDefinition object. It's through this object that you create new BRepCoEdgeDefinition objects.

## Methods

| Name | Description |
|----|----|
| [add](BRepCoEdgeDefinitions_add.md) | Creates a new BrepCoEdgeDefinition object associated with the parent BrepLoopDefinition object. |
| [classType](BRepCoEdgeDefinitions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepCoEdgeDefinitions_item.md) | Function that returns the specified BRepCoEdgeDefinition object using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepCoEdgeDefinitions_count.md) | The number of B-Rep co-edge definition objects in the collection. |
| [isValid](BRepCoEdgeDefinitions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepCoEdgeDefinitions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepLoopDefinition.bRepCoEdgeDefinitions](BRepLoopDefinition_bRepCoEdgeDefinitions.md)

## Version

Introduced in version September 2020  

