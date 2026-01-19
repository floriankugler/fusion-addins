# TwoSidesDistanceExtentDefinition Object

Derived from: [ExtentDefinition](ExtentDefinition.md) Object  

## Description

This object is retired. See more information in the 'Remarks' section below.  

Defines the inputs for a TwoSidesDistanceExtentDefinition object. This defines a feature extent where the distance in each direction can be a different value.

## Remarks

This object is retired. Extents are now defined independently for both directions. To get the equivalent of what this object provided, you will create a DistanceExtentDefinition for each direction and use the when creating the extrusion.

## Methods

| Name | Description |
|----|----|
| [classType](TwoSidesDistanceExtentDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [distanceOne](TwoSidesDistanceExtentDefinition_distanceOne.md) | Gets the ModelParameter that defines the first distance |
| [distanceTwo](TwoSidesDistanceExtentDefinition_distanceTwo.md) | Gets the ModelParameter that defines the second distance |
| [isValid](TwoSidesDistanceExtentDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TwoSidesDistanceExtentDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFeature](TwoSidesDistanceExtentDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |

## Version

Introduced in version August 2014  

