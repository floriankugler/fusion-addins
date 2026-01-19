# Status Object

Derived from: [Base](Base.md) Object  

## Description

Used to communicate the current status of an object or operation. This provides the status and any error messages that might accompany an error or warning.

## Methods

| Name | Description |
|----|----|
| [classType](Status_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isError](Status_isError.md) | If true, An error occurred that has prevented the operation from successfully completing. This takes into account all of the child status messages. |
| [isOK](Status_isOK.md) | If true, the operation was successful without any warnings or errors. This takes into account all of the child status messages. |
| [isValid](Status_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isWarning](Status_isWarning.md) | If true, the operation has succeeded but with an unusual result. This takes into account all of the child status messages. |
| [objectType](Status_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [statusMessages](Status_statusMessages.md) | the status messages associated with this status. These messages are displayed to the user in the alert dialog. Each status message can have children status messages that will be displayed as a tree structure in the alert dialog. |

## Accessed From

[CustomFeatureEventArgs.computeStatus](CustomFeatureEventArgs_computeStatus.md), [DataEventArgs.status](DataEventArgs_status.md)

## Version

Introduced in version July 2021  

