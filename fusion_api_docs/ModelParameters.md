# ModelParameters Object

Derived from: [Base](Base.md) Object  

## Description

Provides access to the Model Parameters within a component.

## Methods

| Name | Description |
|----|----|
| [classType](ModelParameters_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](ModelParameters_item.md) | Function that returns the specified Model Parameter using an index into the collection. |
| [itemByName](ModelParameters_itemByName.md) | Function that returns the specified Model Parameter using the name of the parameter as it is displayed in the parameters dialog. |

## Properties

| Name | Description |
| --- | --- |
| [component](ModelParameters_component.md) | Returns the component that owns the Model Parameters collection |
| [count](ModelParameters_count.md) | Returns the number of parameters in the collection. |
| [isValid](ModelParameters_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ModelParameters_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.modelParameters](Component_modelParameters.md), [CustomFeatureParameter.modelParameters](CustomFeatureParameter_modelParameters.md), [FlatPatternComponent.modelParameters](FlatPatternComponent_modelParameters.md), [ModelParameter.modelParameters](ModelParameter_modelParameters.md)

## Version

Introduced in version August 2014  

