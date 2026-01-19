# KeyboardEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

Provides a set of arguments from a firing KeyboardEvent to a KeyboardEventHandler's notify callback method.

## Methods

| Name | Description |
|----|----|
| [classType](KeyboardEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [firingEvent](KeyboardEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](KeyboardEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [keyCode](KeyboardEventArgs_keyCode.md) | Gets the keyboard key. |
| [modifierMask](KeyboardEventArgs_modifierMask.md) | Gets the set of keyboard modifiers that were active. The value is the Boolean combination of KeyboardModifiers values. |
| [objectType](KeyboardEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2014  

