# CameraEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The CameraEventArgs provides information associated with a camera change. Camera changes happen when user changes the view by rotating, zooming in or out, panning, changing from parallel to perspective, or when the extents of the viewport changes.

## Methods

| Name | Description |
|----|----|
| [classType](CameraEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [firingEvent](CameraEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](CameraEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CameraEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [viewport](CameraEventArgs_viewport.md) | Returns the viewport that the modified camera is associated with. |

## Version

Introduced in version December 2017  

