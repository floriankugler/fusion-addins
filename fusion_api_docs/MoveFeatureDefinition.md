# MoveFeatureDefinition Object

Derived from: [Base](Base.md) Object  

## Description

A Base class to return the information used to define a Move feature.

## Methods

| Name | Description |
|----|----|
| [classType](MoveFeatureDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MoveFeatureDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MoveFeatureDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentMoveFeature](MoveFeatureDefinition_parentMoveFeature.md) | Returns the parent MoveFeature object |

## Accessed From

[MoveFeature.definition](MoveFeature_definition.md)

## Derived Classes

[MoveFeatureFreeMoveDefinition](MoveFeatureFreeMoveDefinition.md), [MoveFeaturePointToPointDefinition](MoveFeaturePointToPointDefinition.md), [MoveFeaturePointToPositionDefinition](MoveFeaturePointToPositionDefinition.md), [MoveFeatureRotateDefinition](MoveFeatureRotateDefinition.md), [MoveFeatureTranslateAlongEntityDefinition](MoveFeatureTranslateAlongEntityDefinition.md), [MoveFeatureTranslateXYZDefinition](MoveFeatureTranslateXYZDefinition.md)

## Version

Introduced in version January 2023  

