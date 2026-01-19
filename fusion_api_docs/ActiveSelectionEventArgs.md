# ActiveSelectionEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The ActiveSelectionEventArgs provides information associated with the active selection changing. The event fires whenever the contents of the active selection changes. This occurs as the user selects or unselects entities while using the Fusion Select command. The Select command is the default command that is always running if no other command is active. Pressing Escape terminates the currently active command and starts the Select command. If the Select command is running and you press Escape, it terminates the current Select command and starts a new one.  

An array or list of all the currently selected entities is returned. This is the same set of entities accessed through the UserInterface.activeSelection object. An empty array can be returned in the case where the selection has been cleared which can occur by the user unselecting and entity, terminating the select command pressing Escape or running another command or clicking the mouse in an open area of the canvas.

## Methods

| Name | Description |
|----|----|
| [classType](ActiveSelectionEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [currentSelection](ActiveSelectionEventArgs_currentSelection.md) | The list of all of the current selections. This is the same set of selections accessed through the UserInterface.activeSelection object. An empty array can be returned in the case where the selection has been cleared which can occur by the user unselecting and entity, terminating the select command pressing Escape or running another command or clicking the mouse in an open area of the canvas. |
| [firingEvent](ActiveSelectionEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](ActiveSelectionEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ActiveSelectionEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Version

Introduced in version August 2020  

