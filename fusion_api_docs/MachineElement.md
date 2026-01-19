# MachineElement Object

Derived from: [Base](Base.md) Object  

## Description

Base class for objects that compose a machine.

## Methods

| Name | Description |
|----|----|
| [classType](MachineElement_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [elementId](MachineElement_elementId.md) | Identifier for this element. Unique within an element type. |
| [isValid](MachineElement_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineElement_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [typeId](MachineElement_typeId.md) | Identifier for this type of machine element. |

## Accessed From

[MachineElements.addElement](MachineElements_addElement.md), [MachineElements.defaultItemByType](MachineElements_defaultItemByType.md), [MachineElements.item](MachineElements_item.md), [MachineElements.itemById](MachineElements_itemById.md), [MachineElements.itemsByType](MachineElements_itemsByType.md)

## Derived Classes

[AdditiveFFFLimitsMachineElement](AdditiveFFFLimitsMachineElement.md), [AdditivePlatformMachineElement](AdditivePlatformMachineElement.md), [ControllerConfigurationMachineElement](ControllerConfigurationMachineElement.md), [ExtruderMachineElement](ExtruderMachineElement.md), [InteractionsMachineElement](InteractionsMachineElement.md), [KinematicsMachineElement](KinematicsMachineElement.md), [MultiAxisMachineElement](MultiAxisMachineElement.md), [PostProcessingMachineElement](PostProcessingMachineElement.md), [ToolingCapabilitiesMachineElement](ToolingCapabilitiesMachineElement.md)

## Version

Introduced in version April 2023  

