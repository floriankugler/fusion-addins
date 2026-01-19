# AsBuiltJoints Object

Derived from: [Base](Base.md) Object  

## Description

The collection of as-built joints in this component. This provides access to all existing as-built joints and supports the ability to create new as-built joints.

## Methods

| Name | Description |
|----|----|
| [add](AsBuiltJoints_add.md) | Creates a new as-built joint. |
| [classType](AsBuiltJoints_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInput](AsBuiltJoints_createInput.md) | Creates an AsBuiltJointInput object which is used to collect all of the information needed to create an as-built joint. This object is equivalent to the as-built joint dialog in the user-interface in that it doesn't represent an actual joint but just the information needed to create an as-built joint. Once this is fully defined the add method can be called, passing this object in to create the actual joint. |
| [item](AsBuiltJoints_item.md) | Function that returns the specified as-built joint using an index into the collection. |
| [itemByName](AsBuiltJoints_itemByName.md) | Function that returns the specified as-built joint using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](AsBuiltJoints_count.md) | Returns number of joint origins in the collection. |
| [isValid](AsBuiltJoints_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](AsBuiltJoints_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.asBuiltJoints](Component_asBuiltJoints.md), [FlatPatternComponent.asBuiltJoints](FlatPatternComponent_asBuiltJoints.md)

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |

## Version

Introduced in version September 2015  

