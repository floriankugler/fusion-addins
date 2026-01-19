# AreaProperties Object

Derived from: [Base](Base.md) Object  

## Description

The Area properties of a sketch profile or planar surface.

## Methods

| Name | Description |
|----|----|
| [classType](AreaProperties_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getCentroidMomentsOfInertia](AreaProperties_getCentroidMomentsOfInertia.md) | Method that returns the moments of inertia about the centroid. Unit for returned values is kg\*cm^2. |
| [getMomentsOfInertia](AreaProperties_getMomentsOfInertia.md) | Method that, for a sketch, returns the moments of inertia about the sketch origin. For a planar face, this method returns the moments about the world coordinate system origin. Unit for returned values is kg\*cm^2. |
| [getPrincipalAxes](AreaProperties_getPrincipalAxes.md) | Method that returns the principal axes. |
| [getPrincipalMomentsOfInertia](AreaProperties_getPrincipalMomentsOfInertia.md) | Method that returns the moments of inertia about the principal axes. Unit for returned values is kg\*cm^2. |
| [getRadiusOfGyration](AreaProperties_getRadiusOfGyration.md) | Method that returns the radius of gyration about the principal axes. Unit for returned values is cm. |

## Properties

| Name | Description |
| --- | --- |
| [accuracy](AreaProperties_accuracy.md) | Returns the accuracy that was used for the calculation. |
| [area](AreaProperties_area.md) | Gets the area in the square centimeters. |
| [centroid](AreaProperties_centroid.md) | Gets the centroid where the units are centimeters. The Location is relative to the sketch origin for a profile or relative to the world coordinate system for a planar face. |
| [isValid](AreaProperties_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AreaProperties_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [perimeter](AreaProperties_perimeter.md) | Gets the perimeter in centimeters. The perimeter is the sum of the length of all the curves or edges of the profile or planar surface |
| [rotationToPrincipal](AreaProperties_rotationToPrincipal.md) | Gets the angle of rotation of the principal axes. |

## Accessed From

[Design.areaProperties](Design_areaProperties.md), [FlatPatternProduct.areaProperties](FlatPatternProduct_areaProperties.md), [Profile.areaProperties](Profile_areaProperties.md), [WorkingModel.areaProperties](WorkingModel_areaProperties.md)

## Samples

| Name | Description |
|----|----|
| [API Sample for AreaProperties](AreaPropertiesSample_Sample.md) | Demonstrates how to use AreaProperties |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version March 2016  

