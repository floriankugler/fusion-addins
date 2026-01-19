
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Collection that provides access to all of the existing custom features in a component and supports the ability to create new custom features.

## Methods

| Name | Description |
|----|----|
| [add](CustomFeatures_add.md) | Creates a new custom feature. |
| [classType](CustomFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](CustomFeatures_createInput.md) | Creates a new input object that you use to define a custom feature. Creating an input object doesn't create the feature but provides a way to gather all of the input needed to create a custom feature. To create the custom feature, the fully defined input object is passed to the add method. |
| [item](CustomFeatures_item.md) | Function that returns the specified ruled surface feature using an index into the collection. |
| [itemByName](CustomFeatures_itemByName.md) | Function that returns the specified CustomFeature feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](CustomFeatures_count.md) | The number of CustomFeature objects in the collection. |
| [isValid](CustomFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CustomFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.customFeatures](Features_customFeatures.md)

## Version

Introduced in version January 2021  

