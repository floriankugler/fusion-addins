# MeasureResults Object

Derived from: [Base](Base.md) Object  

## Description

Provides measurement results from the various measurement methods available on the MeasureManager object.

## Methods

| Name | Description |
|----|----|
| [classType](MeasureResults_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MeasureResults_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MeasureResults_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [positionOne](MeasureResults_positionOne.md) | For a distance measurement, this is the point on the first entity where the measurement was made from. For an angle measurement this is one of the three points defining the angle. |
| [positionThree](MeasureResults_positionThree.md) | This point is only used for angle measurements and is one of the three points defining the angle. |
| [positionTwo](MeasureResults_positionTwo.md) | For a distance measurement, this is the point on the second entity where the measurement was made to. For an angle measurement this is one of the three points defining the angle. |
| [value](MeasureResults_value.md) | The measurement value. If the measurement is a distance this value will be in centimeters. If it's an angle then it will be in radians. |

## Accessed From

[MeasureManager.measureAngle](MeasureManager_measureAngle.md), [MeasureManager.measureMinimumDistance](MeasureManager_measureMinimumDistance.md)

## Samples

| Name                                       | Description               |
|--------------------------------------------|---------------------------|
| [Measure Sample](MeasureSample_Sample.md) | Measure related functions |

## Version

Introduced in version December 2017  

