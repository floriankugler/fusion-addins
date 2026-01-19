# RevolveFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing revolve features in a design and supports the ability to create new revolve features.

## Methods

| Name | Description |
|----|----|
| [add](RevolveFeatures_add.md) | Creates a new revolve feature based on the information provided by the provided RevolveFeatureInput object. To create a new revolve, use the createInput function to create a new input object and then use the methods and properties on that object to define the required input for a revolve. Once the information is defined on the input object you can pass it to the Add method to create the revolve. |
| [classType](RevolveFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](RevolveFeatures_createInput.md) | Creates a new RevolveFeatureInput object that is used to specify the input needed to create a new revolve feature. |
| [item](RevolveFeatures_item.md) | Function that returns the specified revolve feature using an index into the collection. |
| [itemByName](RevolveFeatures_itemByName.md) | Function that returns the specified revolve feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](RevolveFeatures_count.md) | The number of revolve features in the collection. |
| [isValid](RevolveFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RevolveFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.revolveFeatures](Features_revolveFeatures.md)

## Samples

| Name | Description |
|----|----|
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

