# MotionLinks Object

Derived from: [Base](Base.md) Object  

## Description

The collection of MotionLinks in this component. This provides access to all existing MotionLinks and supports the ability to create new MotionLinks.

## Methods

| Name | Description |
|----|----|
| [add](MotionLinks_add.md) | Creates a new MotionLink. |
| [classType](MotionLinks_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](MotionLinks_createInput.md) | Creates a MotionLinkInput object, which is the API equivalent to the Motion Link command dialog. You can use methods and properties on the returned object to set the desired options, similar to providing input and setting options in the MotionLink command dialog. Once the settings are defined you call the MotionLinks.add method passing in the MotionLinkInput object to create the actual MotionLink. |
| [item](MotionLinks_item.md) | Function that returns the specified MotionLink using an index into the collection. |
| [itemByName](MotionLinks_itemByName.md) | Function that returns the specified MotionLink using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](MotionLinks_count.md) | Returns number of MotionLinks in the collection. |
| [isValid](MotionLinks_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MotionLinks_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.motionLinks](Component_motionLinks.md), [FlatPatternComponent.motionLinks](FlatPatternComponent_motionLinks.md)

## Version

Introduced in version November 2025  

