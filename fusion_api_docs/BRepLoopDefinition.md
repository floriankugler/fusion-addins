# BRepLoopDefinition Object

Derived from: [Base](Base.md) Object  

## Description

Represents the definition of a B-Rep loop that can be used as input to create a BRepBody that includes this loop.

## Methods

| Name | Description |
|----|----|
| [classType](BRepLoopDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [bRepCoEdgeDefinitions](BRepLoopDefinition_bRepCoEdgeDefinitions.md) | Provides access to the BRepCoEdgeDefinitions object associated with the parent BRepFaceDefinition object. It's through the returned collection that you can create new BRepCoEdgeDefinition objects. |
| [isValid](BRepLoopDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepLoopDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepLoopDefinitions.add](BRepLoopDefinitions_add.md), [BRepLoopDefinitions.item](BRepLoopDefinitions_item.md)

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

