# ActiveSelectionEvent Object

Derived from: [Event](Event.md) Object  

## Description

This event fires whenever the contents of the active selection changes. This occurs as the user selects or unselects entities while using the Fusion Select command. The Select command is the default command that is always running if no other command is active. Pressing Escape terminates the currently active command and starts the Select command. If the Select command is running and you press Escape, it terminates the current Select command and starts a new one.  

This event is only associated with the selection associated with the Select command and does not fire when any other command is running. The event fires when there is any change to the active selection, including when the selection is cleared when the Select command is terminated. It is also fired when the user clicks in an open area of the canvas to clear the current selection.

## Methods

| Name | Description |
|----|----|
| [add](ActiveSelectionEvent_add.md) | Add a handler to be notified when the event occurs. |
| [classType](ActiveSelectionEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](ActiveSelectionEvent_remove.md) | Removes a handler from the event. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ActiveSelectionEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](ActiveSelectionEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](ActiveSelectionEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](ActiveSelectionEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[UserInterface.activeSelectionChanged](UserInterface_activeSelectionChanged.md)

## Version

Introduced in version August 2020  

