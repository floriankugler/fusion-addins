# SetupEvent Object

Derived from: [Event](Event.md) Object  

## Description

A SetupEvent represents a setup related event. For example, SetupCreated or SetupDestroying.

## Methods

| Name | Description |
|----|----|
| [add](SetupEvent_add.md) | Add a handler to be notified when the file event occurs. |
| [classType](SetupEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](SetupEvent_remove.md) | Removes a handler from the event. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](SetupEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](SetupEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](SetupEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](SetupEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[CAM.setupActivated](CAM_setupActivated.md), [CAM.setupActivating](CAM_setupActivating.md), [CAM.setupCreated](CAM_setupCreated.md), [CAM.setupDeactivated](CAM_setupDeactivated.md), [CAM.setupDeactivating](CAM_setupDeactivating.md), [CAM.setupDestroying](CAM_setupDestroying.md)

## Version

Introduced in version April 2023  

