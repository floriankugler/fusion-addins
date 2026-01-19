# DocumentEvent Object

Derived from: [Event](Event.md) Object  

## Description

A DocumentEvent represents a document related event. For example, DocumentOpening or DocumentOpened.

## Methods

| Name | Description |
|----|----|
| [add](DocumentEvent_add.md) | Add a handler to be notified when the file event occurs. |
| [classType](DocumentEvent_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [remove](DocumentEvent_remove.md) | Removes a handler from the event. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](DocumentEvent_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](DocumentEvent_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](DocumentEvent_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](DocumentEvent_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[Application.documentActivated](Application_documentActivated.md), [Application.documentActivating](Application_documentActivating.md), [Application.documentClosed](Application_documentClosed.md), [Application.documentClosing](Application_documentClosing.md), [Application.documentCreated](Application_documentCreated.md), [Application.documentDeactivated](Application_documentDeactivated.md), [Application.documentDeactivating](Application_documentDeactivating.md), [Application.documentOpened](Application_documentOpened.md), [Application.documentOpening](Application_documentOpening.md), [Application.documentSaved](Application_documentSaved.md), [Application.documentSaving](Application_documentSaving.md)

## Version

Introduced in version August 2014  

