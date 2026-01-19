# MeasureManager Object

Derived from: [Base](Base.md) Object  

## Description

The MeasurementManager class provides some generic measurement utilities that can be used for most entity types.

## Methods

| Name | Description |
| --- | --- |
| [classType](MeasureManager_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getOrientedBoundingBox](MeasureManager_getOrientedBoundingBox.md) | Calculates an oriented bounding box for the input geometry. The bounding box is tight fitting to the input geometry and is particularly useful when you want to calculate a bounding box that is not oriented to be parallel to the model x-y-z plane. The height direction is automatically determined using the length and width directions. |
| [measureAngle](MeasureManager_measureAngle.md) | Measures the angle between the input geometry. |
| [measureMinimumDistance](MeasureManager_measureMinimumDistance.md) | Measures the minimum distance between the two input geometries. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MeasureManager_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MeasureManager_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Application.measureManager](Application_measureManager.md)

## Samples

| Name                                       | Description               |
|--------------------------------------------|---------------------------|
| [Measure Sample](MeasureSample_Sample.md) | Measure related functions |

## Version

Introduced in version December 2017  

