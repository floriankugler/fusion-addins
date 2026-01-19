# BRepFaceDefinition Object

Derived from: [Base](Base.md) Object  

## Description

Represents the definition of a B-Rep face that can be used as input to create a BRepBody that includes this face.

## Methods

| Name | Description |
|----|----|
| [classType](BRepFaceDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [associativeID](BRepFaceDefinition_associativeID.md) | Gets and sets the associate ID of this face definition. This ID will be copied to the corresponding face when the BRepBodyDefinition is used to create a BrepBody. It is used by Fusion as the identifier for the face and is used for tracking this geometry for parametric recomputes. |
| [isParamReversed](BRepFaceDefinition_isParamReversed.md) | Gets and sets if the normal of this face is reversed with respect to the surface geometry associated with this face definition. |
| [isValid](BRepFaceDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [loopDefinitions](BRepFaceDefinition_loopDefinitions.md) | Provides access to the BRepLoopDefinitions object associated with this BRepFaceDefinition. It's through the returned collection that you can create new BRepLoopDefinition objects. |
| [objectType](BRepFaceDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [surfaceGeometry](BRepFaceDefinition_surfaceGeometry.md) | Gets and sets the surface geometry associated with this face definition. |

## Accessed From

[BRepFaceDefinitions.add](BRepFaceDefinitions_add.md), [BRepFaceDefinitions.item](BRepFaceDefinitions_item.md)

## Samples

| Name | Description |
|----|----|
| [BRep Body definition Sample](BRepBodyDefinition_Sample.md) | Demonstrates creating BRep bodies by BRepBodyDefinition. |

## Version

Introduced in version September 2020  

