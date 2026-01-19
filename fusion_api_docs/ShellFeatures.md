# ShellFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing shell features in a component and supports the ability to create new shell features.

## Methods

| Name | Description |
|----|----|
| [add](ShellFeatures_add.md) | Creates a new shell feature. |
| [classType](ShellFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](ShellFeatures_createInput.md) | Creates a ShellFeatureInput object. Use properties and methods on this object to define the shell you want to create and then use the Add method, passing in the ShellFeatureInput object. |
| [item](ShellFeatures_item.md) | Function that returns the specified shell feature using an index into the collection. |
| [itemByName](ShellFeatures_itemByName.md) | Function that returns the specified shell feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](ShellFeatures_count.md) | The number of shell features in the collection. |
| [isValid](ShellFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ShellFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.shellFeatures](Features_shellFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Shell Feature API Sample](ShellFeatureSample_Sample.md) | Demonstrates creating a new shell feature. |

## Version

Introduced in version November 2014  

