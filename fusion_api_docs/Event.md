# Event Object

Derived from: [Base](Base.md) Object  

## Description

Objects can have several Event properties that fire when some 'event' occurs. Clients can attach EventHandlers to one or more Events and they get notified when the 'event' occurs.  

This is a base class - classes like DocumentEvent add type safety (i.e. only allow the correct type of handler to be added to them).

## Methods

| Name | Description |
|----|----|
| [classType](Event_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Event_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](Event_name.md) | The name of the event - e.g. "DocumentOpening" |
| [objectType](Event_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sender](Event_sender.md) | The object that is firing the event. For example, in the case of a command input event this will return the command. |

## Accessed From

[ActiveSelectionEventArgs.firingEvent](ActiveSelectionEventArgs_firingEvent.md), [ApplicationCommandEventArgs.firingEvent](ApplicationCommandEventArgs_firingEvent.md), [ApplicationEventArgs.firingEvent](ApplicationEventArgs_firingEvent.md), [CameraEventArgs.firingEvent](CameraEventArgs_firingEvent.md), [CommandCreatedEventArgs.firingEvent](CommandCreatedEventArgs_firingEvent.md), [CommandEventArgs.firingEvent](CommandEventArgs_firingEvent.md), [CustomEventArgs.firingEvent](CustomEventArgs_firingEvent.md), [CustomFeatureEventArgs.firingEvent](CustomFeatureEventArgs_firingEvent.md), [DataEventArgs.firingEvent](DataEventArgs_firingEvent.md), [DocumentEventArgs.firingEvent](DocumentEventArgs_firingEvent.md), [EventArgs.firingEvent](EventArgs_firingEvent.md), [HTMLEventArgs.firingEvent](HTMLEventArgs_firingEvent.md), [HttpEventArgs.firingEvent](HttpEventArgs_firingEvent.md), [InputChangedEventArgs.firingEvent](InputChangedEventArgs_firingEvent.md), [KeyboardEventArgs.firingEvent](KeyboardEventArgs_firingEvent.md), [MarkingMenuEventArgs.firingEvent](MarkingMenuEventArgs_firingEvent.md), [MFGDMDataEventArgs.firingEvent](MFGDMDataEventArgs_firingEvent.md), [MouseEventArgs.firingEvent](MouseEventArgs_firingEvent.md), [NavigationEventArgs.firingEvent](NavigationEventArgs_firingEvent.md), [RenderEventArgs.firingEvent](RenderEventArgs_firingEvent.md), [SelectionEventArgs.firingEvent](SelectionEventArgs_firingEvent.md), [SetupChangeEventArgs.firingEvent](SetupChangeEventArgs_firingEvent.md), [SetupEventArgs.firingEvent](SetupEventArgs_firingEvent.md), [UserInterfaceGeneralEventArgs.firingEvent](UserInterfaceGeneralEventArgs_firingEvent.md), [ValidateInputsEventArgs.firingEvent](ValidateInputsEventArgs_firingEvent.md), [WebRequestEventArgs.firingEvent](WebRequestEventArgs_firingEvent.md), [WorkspaceEventArgs.firingEvent](WorkspaceEventArgs_firingEvent.md)

## Derived Classes

[ActiveSelectionEvent](ActiveSelectionEvent.md), [ApplicationCommandEvent](ApplicationCommandEvent.md), [ApplicationEvent](ApplicationEvent.md), [CameraEvent](CameraEvent.md), [CommandCreatedEvent](CommandCreatedEvent.md), [CommandEvent](CommandEvent.md), [CustomEvent](CustomEvent.md), [CustomFeatureEvent](CustomFeatureEvent.md), [DataEvent](DataEvent.md), [DocumentEvent](DocumentEvent.md), [HTMLEvent](HTMLEvent.md), [HttpEvent](HttpEvent.md), [InputChangedEvent](InputChangedEvent.md), [KeyboardEvent](KeyboardEvent.md), [MarkingMenuEvent](MarkingMenuEvent.md), [MFGDMDataEvent](MFGDMDataEvent.md), [MouseEvent](MouseEvent.md), [NavigationEvent](NavigationEvent.md), [RenderEvent](RenderEvent.md), [SelectionEvent](SelectionEvent.md), [SetupChangeEvent](SetupChangeEvent.md), [SetupEvent](SetupEvent.md), [UserInterfaceGeneralEvent](UserInterfaceGeneralEvent.md), [ValidateInputsEvent](ValidateInputsEvent.md), [WebRequestEvent](WebRequestEvent.md), [WorkspaceEvent](WorkspaceEvent.md)

## Version

Introduced in version August 2014  

