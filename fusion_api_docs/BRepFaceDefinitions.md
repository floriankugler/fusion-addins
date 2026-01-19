# BRepFaceDefinitions Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the BRepFaceDefinition objects associated with the object the collection was obtained from. It's through this object that you create new BRepFaceDefinition objects.

## Methods

| Name | Description |
|----|----|
| [add](BRepFaceDefinitions_add.md) | Creates a new BrepFaceDefinition within the parent BRepShellDefinition object. |
| [classType](BRepFaceDefinitions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](BRepFaceDefinitions_item.md) | Function that returns the specified BRepFaceDefinition object using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](BRepFaceDefinitions_count.md) | The number of B-Rep face definition objects in the collection. |
| [isValid](BRepFaceDefinitions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](BRepFaceDefinitions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepShellDefinition.faceDefinitions](BRepShellDefinition_faceDefinitions.md)

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

