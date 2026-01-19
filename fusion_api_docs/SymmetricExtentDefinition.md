# SymmetricExtentDefinition Object

Derived from: [ExtentDefinition](ExtentDefinition.md) Object  

## Description

A definition object that is used to define the extents of a feature to be symmetric.

## Methods

| Name | Description |
|----|----|
| [classType](SymmetricExtentDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](SymmetricExtentDefinition_create.md) | Statically creates a new SymmetricExtentDefinition object. This is used as input when create a new feature and defining the starting condition. |

## Properties

| Name | Description |
| --- | --- |
| [distance](SymmetricExtentDefinition_distance.md) | Returns the current extent distance. If the SymmetricExtentDefinition object has been created statically and isn't associated with a feature this will return a ValueInput object. If the SymmetricExtentDefinition object is obtained from a feature this will return a ModelParameter object. You can use properties of the parameter to edit its value which will result in the feature updating. |
| [isFullLength](SymmetricExtentDefinition_isFullLength.md) | Gets and sets if the distance defines the full extent length or half the length. A value of True indicates if defines the full length. |
| [isValid](SymmetricExtentDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SymmetricExtentDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFeature](SymmetricExtentDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |
| [taperAngle](SymmetricExtentDefinition_taperAngle.md) | Returns the current taper angle. If the SymmetricExtentDefinition object has been created statically and isn't associated with a feature this will return a ValueInput object. If the SymmetricExtentDefinition object is obtained from a feature this will return a ModelParameter object. You can use properties of the parameter to edit its value which will result in the feature updating. |

## Accessed From

[ExtrudeFeature.symmetricExtent](ExtrudeFeature_symmetricExtent.md), [SymmetricExtentDefinition.create](SymmetricExtentDefinition_create.md)

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

