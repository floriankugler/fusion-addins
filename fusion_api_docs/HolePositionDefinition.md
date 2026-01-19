# HolePositionDefinition Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the classes that define how a hole can be positioned.

## Methods

| Name | Description |
|----|----|
| [classType](HolePositionDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](HolePositionDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](HolePositionDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[HoleFeature.holePositionDefinition](HoleFeature_holePositionDefinition.md)

## Derived Classes

[AtCenterHolePositionDefinition](AtCenterHolePositionDefinition.md), [OnEdgeHolePositionDefinition](OnEdgeHolePositionDefinition.md), [PlaneAndOffsetsHolePositionDefinition](PlaneAndOffsetsHolePositionDefinition.md), [PointHolePositionDefinition](PointHolePositionDefinition.md), [SketchPointHolePositionDefinition](SketchPointHolePositionDefinition.md), [SketchPointsHolePositionDefinition](SketchPointsHolePositionDefinition.md)

## Version

Introduced in version August 2014  

