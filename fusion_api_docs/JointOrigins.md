# JointOrigins Object

Derived from: [Base](Base.md) Object  

## Description

The collection of joint origins in this component. This provides access to all existing joint origins and supports the ability to create new joint origins.

## Methods

| Name | Description |
|----|----|
| [add](JointOrigins_add.md) | Create a new joint origin. |
| [classType](JointOrigins_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](JointOrigins_createInput.md) | Creates a JointOriginInput object which is used to collect all of the information needed to create a simple joint origin. The creation of the input object takes the required input as the geometry argument and you can optionally use methods and properties on the created JointOriginInput to set other optional settings. The JointOrigin is created by calling the add method of the JointOrigins object and passing it the JointOriginInput object. |
| [item](JointOrigins_item.md) | Function that returns the specified joint origin using an index into the collection. |
| [itemByName](JointOrigins_itemByName.md) | Function that returns the specified joint origin using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](JointOrigins_count.md) | Returns number of joint origins in the collection. |
| [isValid](JointOrigins_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](JointOrigins_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.jointOrigins](Component_jointOrigins.md), [FlatPatternComponent.jointOrigins](FlatPatternComponent_jointOrigins.md)

## Samples

| Name | Description |
|----|----|
| [Joint Origin Between Two Faces Sample](JointOrigin2Planes_Sample.md) | Demonstrates creating a new Joint Origin between two planes. |
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |

## Version

Introduced in version September 2015  

