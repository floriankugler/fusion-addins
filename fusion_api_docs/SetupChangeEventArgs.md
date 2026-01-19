# SetupChangeEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The SetupChangeEventArgs provides information associated with a change event of a setup.

## Methods

| Name | Description |
|----|----|
| [classType](SetupChangeEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [firingEvent](SetupChangeEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [info](SetupChangeEventArgs_info.md) | Provides access to an information string. The optional string may contain additional information about the change. |
| [isValid](SetupChangeEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SetupChangeEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [setup](SetupChangeEventArgs_setup.md) | Provides access to the setup. Can be null in the case where the event is fired before the setup has been created or after it has been deleted. |
| [type](SetupChangeEventArgs_type.md) | The type specifies the actual change. |

## Version

Introduced in version April 2023  

