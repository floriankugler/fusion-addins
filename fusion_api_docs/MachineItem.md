
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

An item on a machine that can collide. That is, a MachinePart, or something attached to a MachinePart. Create them via InteractionsMachineElement::createMachineItem

## Methods

| Name | Description |
|----|----|
| [classType](MachineItem_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](MachineItem_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [itemType](MachineItem_itemType.md) | The type of this MachineItem. |
| [objectType](MachineItem_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [part](MachineItem_part.md) | The machine part. |

## Accessed From

[InteractionsMachineElement.createMachineItem](InteractionsMachineElement_createMachineItem.md), [MachineInteractionPair.item1](MachineInteractionPair_item1.md), [MachineInteractionPair.item2](MachineInteractionPair_item2.md)

## Version

Introduced in version September 2025  

