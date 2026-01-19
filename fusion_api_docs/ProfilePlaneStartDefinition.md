# ProfilePlaneStartDefinition Object

Derived from: [ExtentDefinition](ExtentDefinition.md) Object  

## Description

A definition object that is used to define a feature whose start plane is the sketch plane of the profile.

## Methods

| Name | Description |
|----|----|
| [classType](ProfilePlaneStartDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](ProfilePlaneStartDefinition_create.md) | Statically creates a new ProfilePlaneStartDefinition object. This is used as input when creating a new feature and defining the starting condition. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ProfilePlaneStartDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ProfilePlaneStartDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFeature](ProfilePlaneStartDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |
| [profilePlane](ProfilePlaneStartDefinition_profilePlane.md) | Returns the geometric definition of the profile plane. |

## Accessed From

[ProfilePlaneStartDefinition.create](ProfilePlaneStartDefinition_create.md)

## Samples

| Name | Description |
|----|----|
| [extrudeFeatures.add using thin extrude](extrudeFeaturesThin_add_Sample.md) | Demonstrates the extrudeFeatures.add method using the setThinExtrude method. To use this sample have a design open that contains a sketch with a profile. When you run the script you will be prompted to select the profile that will be used to create the thin extrusion. |

## Version

Introduced in version November 2016  

