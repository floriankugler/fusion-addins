# MouseEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

Provides a set of arguments from a firing MouseEvent to a MouseEventHandler's notify callback method.

## Methods

| Name | Description |
|----|----|
| [classType](MouseEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [button](MouseEventArgs_button.md) | Gets which mouse button(s) are pressed. The returned value is bitwise and can indicate that more than one button is pressed. |
| [clicks](MouseEventArgs_clicks.md) | Gets the number of times the button was pressed and released. |
| [firingEvent](MouseEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](MouseEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [keyboardModifiers](MouseEventArgs_keyboardModifiers.md) | Gets which modifier keys are currently pressed. The returned value is bitwise and can indicate that more than one button is pressed. |
| [objectType](MouseEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [position](MouseEventArgs_position.md) | Gets the coordinate of the mouse in screen space. |
| [viewport](MouseEventArgs_viewport.md) | Returns the viewport where the mouse event occurred, if it was within a viewport. If the mouse is not over a viewport this property will return null. |
| [viewportPosition](MouseEventArgs_viewportPosition.md) | Gets the coordinate of the mouse in viewport space, if the mouse is within a viewport. If the mouse is not over a viewport this property will return null. |
| [wheelDelta](MouseEventArgs_wheelDelta.md) | Gets a signed count of the number of detents the mouse wheel has rotated. |

## Version

Introduced in version August 2014  

