# RigidGroups Object

Derived from: [Base](Base.md) Object  

## Description

The collection of rigid groups in this component. This provides access to all existing rigid groups and supports the ability to create new rigid groups.

## Methods

| Name | Description |
|----|----|
| [add](RigidGroups_add.md) | Creates a new rigid group. |
| [classType](RigidGroups_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](RigidGroups_item.md) | Function that returns the specified rigid group using an index into the collection. |
| [itemByName](RigidGroups_itemByName.md) | Function that returns the specified rigid group using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](RigidGroups_count.md) | Returns number of joint origins in the collection. |
| [isValid](RigidGroups_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RigidGroups_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.rigidGroups](Component_rigidGroups.md), [FlatPatternComponent.rigidGroups](FlatPatternComponent_rigidGroups.md)

## Samples

| Name | Description |
|----|----|
| [Rigid Group API Sample](RigidGroupSample_Sample.md) | Demonstrates creating a new Rigid Group. |

## Version

Introduced in version September 2015  

