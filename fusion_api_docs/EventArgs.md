# EventArgs Object

Derived from: [Base](Base.md) Object  

## Description

When an event handler is called, it is passed an EventArgs object that describes the 'event'. This is a base class - classes like DocumentEventArgs add more information on the 'event'.

## Methods

| Name | Description |
|----|----|
| [classType](EventArgs_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [firingEvent](EventArgs_firingEvent.md) | The event that the firing is in response to. |
| [isValid](EventArgs_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](EventArgs_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Derived Classes

[ActiveSelectionEventArgs](ActiveSelectionEventArgs.md), [ApplicationCommandEventArgs](ApplicationCommandEventArgs.md), [ApplicationEventArgs](ApplicationEventArgs.md), [CameraEventArgs](CameraEventArgs.md), [CommandCreatedEventArgs](CommandCreatedEventArgs.md), [CommandEventArgs](CommandEventArgs.md), [CustomEventArgs](CustomEventArgs.md), [CustomFeatureEventArgs](CustomFeatureEventArgs.md), [DataEventArgs](DataEventArgs.md), [DocumentEventArgs](DocumentEventArgs.md), [HTMLEventArgs](HTMLEventArgs.md), [HttpEventArgs](HttpEventArgs.md), [InputChangedEventArgs](InputChangedEventArgs.md), [KeyboardEventArgs](KeyboardEventArgs.md), [MarkingMenuEventArgs](MarkingMenuEventArgs.md), [MFGDMDataEventArgs](MFGDMDataEventArgs.md), [MouseEventArgs](MouseEventArgs.md), [NavigationEventArgs](NavigationEventArgs.md), [RenderEventArgs](RenderEventArgs.md), [SelectionEventArgs](SelectionEventArgs.md), [SetupChangeEventArgs](SetupChangeEventArgs.md), [SetupEventArgs](SetupEventArgs.md), [UserInterfaceGeneralEventArgs](UserInterfaceGeneralEventArgs.md), [ValidateInputsEventArgs](ValidateInputsEventArgs.md), [WebRequestEventArgs](WebRequestEventArgs.md), [WorkspaceEventArgs](WorkspaceEventArgs.md)

## Version

Introduced in version August 2014  

