# StatusMessages Object

Derived from: [Base](Base.md) Object  

## Description

A collection of status messages associated with a Status object. The primary purpose of the messages is to describe the reason for a warning or failure and display the messages in the alert dialog.

## Methods

| Name | Description |
|----|----|
| [addError](StatusMessages_addError.md) | Adds a new error status message to the list of warning and error messages. |
| [addWarning](StatusMessages_addWarning.md) | Adds a new warning status message to the list of warning and error messages. |
| [classType](StatusMessages_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](StatusMessages_item.md) | Returns the specified status message using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](StatusMessages_count.md) | Returns the number of status messages in this collection. |
| [isValid](StatusMessages_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](StatusMessages_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Status.statusMessages](Status_statusMessages.md), [StatusMessage.childStatusMessages](StatusMessage_childStatusMessages.md)

## Version

Introduced in version July 2021  

