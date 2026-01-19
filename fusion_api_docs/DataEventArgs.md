# DataEventArgs Object

Derived from: [EventArgs](EventArgs.md) Object  

## Description

The DataEventArgs provides information associated with a data event. Note that some properties are not available on every event.

## Methods

| Name | Description |
|----|----|
| [classType](DataEventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [file](DataEventArgs_file.md) | Gets the DataFile object associated with this event. If there isn't a DataFile associated with the event, this property will return null. |
| [filename](DataEventArgs_filename.md) | Gets the filename associated with the operation. If there isn't an associated filename, an empty string is returned. For a download operation, this will be the full filename of the downloaded file. |
| [firingEvent](DataEventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](DataEventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](DataEventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [status](DataEventArgs_status.md) | Returns a Status object that provides additional information about the success or failure of the operation. |

## Version

Introduced in version January 2022  

