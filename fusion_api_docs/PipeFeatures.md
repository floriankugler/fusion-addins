# PipeFeatures Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all of the existing Pipe features in a design.

## Methods

| Name | Description |
|----|----|
| [add](PipeFeatures_add.md) | Creates a new Pipe feature. |
| [classType](PipeFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](PipeFeatures_createInput.md) | Creates a PipeFeatureInput object for defining a simple Pipe feature with only a path. Use properties and methods on this object to define the Pipe you want to create and then use the Add method, passing in the PipeFeatureInput object. |
| [item](PipeFeatures_item.md) | Function that returns the specified Pipe feature using an index into the collection. |
| [itemByName](PipeFeatures_itemByName.md) | Function that returns the specified Pipe feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](PipeFeatures_count.md) | The number of Pipe features in the collection. |
| [isValid](PipeFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PipeFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.pipeFeatures](Features_pipeFeatures.md)

## Version

Introduced in version September 2015  

