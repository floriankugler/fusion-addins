# StatusMessage Object

Derived from: [Base](Base.md) Object  

## Description

Defines the message associated with a Status object.

## Methods

| Name | Description |
|----|----|
| [classType](StatusMessage_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [childStatusMessages](StatusMessage_childStatusMessages.md) | Returns the collection of status codes that are children of this status message. |
| [isValid](StatusMessage_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [message](StatusMessage_message.md) | The user visible message being used. Setting this message for custom feature errors or warnings is currently ignored. |
| [messageId](StatusMessage_messageId.md) | Gets and sets the ID of the message being used. This is a predefined ID within the Fusion message string table. |
| [objectType](StatusMessage_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [statusMessageType](StatusMessage_statusMessageType.md) | Returns the type of message this StatusMessage represents. |

## Accessed From

[StatusMessages.addError](StatusMessages_addError.md), [StatusMessages.addWarning](StatusMessages_addWarning.md), [StatusMessages.item](StatusMessages_item.md)

## Version

Introduced in version July 2021  

