# TwoSidesAngleExtentDefinition Object

Derived from: [ExtentDefinition](ExtentDefinition.md) Object  

## Description

Defines the inputs for a TwoSidesAngleExtentDefinition object. This feature extent type defines the extents of the feature using angle extents on two sides.

## Methods

| Name | Description |
|----|----|
| [classType](TwoSidesAngleExtentDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [angleOne](TwoSidesAngleExtentDefinition_angleOne.md) | Gets the ModelParameter that defines the angle on the first side. The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter. |
| [angleTwo](TwoSidesAngleExtentDefinition_angleTwo.md) | Gets the ModelParameter that defines the angle on the second side. The value of the angle can be edited by using the properties on the ModelParameter object to edit the parameter. |
| [isValid](TwoSidesAngleExtentDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](TwoSidesAngleExtentDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFeature](TwoSidesAngleExtentDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |

## Version

Introduced in version August 2014  

