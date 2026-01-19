# HttpEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The HttpEventArgs provides information associated with a http request.

## Methods

| Name | Description |
|----|----|
| [classType](HttpEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [firingEvent](HttpEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](HttpEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](HttpEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [response](HttpEventArgs_response.md) | Returns the response from an http request. |

## Version

Introduced in version January 2024  

