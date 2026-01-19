# OffsetFacesFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Offset Faces features in a design. Offset Face features are created in the UI using the "Offset Face" or "Press Pull" command.

## Methods

| Name | Description |
|----|----|
| [add](OffsetFacesFeatures_add.md) | Creates a new offset feature. |
| [classType](OffsetFacesFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](OffsetFacesFeatures_createInput.md) | Creates an OffsetFacesFeatureInput object. Use properties and methods on this object to define the offset feature you want to create and then use the add method, passing in the OffsetFacesFeatureInput object to create the feature. |
| [item](OffsetFacesFeatures_item.md) | Function that returns the specified Offset Face feature using an index into the collection. |
| [itemByName](OffsetFacesFeatures_itemByName.md) | Function that returns the specified Offset Face feature using the name of the feature. Offset Face features are created in the UI using the "Press Pull" command. |

## Properties

| Name | Description |
| --- | --- |
| [count](OffsetFacesFeatures_count.md) | The number of Offset Face features in the collection. Offset Face features are created in the UI using the "Press Pull" command. |
| [isValid](OffsetFacesFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](OffsetFacesFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.offsetFacesFeatures](Features_offsetFacesFeatures.md)

## Version

Introduced in version June 2017  

