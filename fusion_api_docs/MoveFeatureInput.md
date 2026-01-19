# MoveFeatureInput Object

Derived from: [Base](Base.md) Object  

## Description

This class defines the methods and properties that pertain to the definition of a move feature.

## Methods

| Name | Description |
|----|----|
| [classType](MoveFeatureInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [defineAsFreeMove](MoveFeatureInput_defineAsFreeMove.md) | This method will define a move feature whose translation and orientation is defined using a transformation matrix. A matrix can define any translation and orientation. |
| [defineAsPointToPoint](MoveFeatureInput_defineAsPointToPoint.md) | This method defines a move feature described by a translation from one point to another. |
| [defineAsPointToPosition](MoveFeatureInput_defineAsPointToPosition.md) | This method defines a move feature described by a point and an offset. The distances define offsets in the X, Y, and Z directions in either design or component space. To not move the input entities at all the offset distances should be set to the current location of the point in either design or component space. Adding or subtracting to those values will then move the entities that distance. It's best to experiment with the command interactively to understand the behavior. |
| [defineAsRotate](MoveFeatureInput_defineAsRotate.md) | This method defines a move feature that is described by an axis and rotation angle. |
| [defineAsTranslateAlongEntity](MoveFeatureInput_defineAsTranslateAlongEntity.md) | This method will define a move feature that defines a translation along a specified entity. |
| [defineAsTranslateXYZ](MoveFeatureInput_defineAsTranslateXYZ.md) | This method will define a move feature that defines a translation in X, Y, and Z. |

## Properties

| Name | Description |
| --- | --- |
| [inputEntities](MoveFeatureInput_inputEntities.md) | An ObjectCollection containing the objects to move. The collection can contain BRepBody or BRepFace objects but not a mixture of the two types. |
| [isValid](MoveFeatureInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MoveFeatureInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [targetBaseFeature](MoveFeatureInput_targetBaseFeature.md) | When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature. Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it. |
| [transform](MoveFeatureInput_transform.md) | **RETIRED** Gets and sets the transform to apply to the input entities. This can describe a move (translation) or a rotation. The matrix must define an orthogonal transform. That is the axes remain perpendicular to each other and there isn't any scale or mirror defined. |

## Accessed From

[MoveFeatures.createInput](MoveFeatures_createInput.md), [MoveFeatures.createInput2](MoveFeatures_createInput2.md)

## Samples

| Name | Description |
|----|----|
| [Move Feature API Sample](MoveFeatureSample_Sample.md) | Demonstrates creating a new move feature. |

## Version

Introduced in version March 2015  

