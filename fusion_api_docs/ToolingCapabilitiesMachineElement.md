
Derived from: [MachineElement](MachineElement.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Machine element representing the tooling capabilities of a machine.

## Methods

| Name | Description |
|----|----|
| [classType](ToolingCapabilitiesMachineElement_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [staticTypeId](ToolingCapabilitiesMachineElement_staticTypeId.md) | Identifying name for all elements of this type. Pass this to the itemByType or itemById methods of MachineElements to filter to elements of this type. |

## Properties

| Name | Description |
| --- | --- |
| [elementId](ToolingCapabilitiesMachineElement_elementId.md) | Identifier for this element. Unique within an element type. |
| [isToolChangerAutomatic](ToolingCapabilitiesMachineElement_isToolChangerAutomatic.md) | If your machine has an automatic tool changer, set this to true. For machines with manual tool change capabilities, set this to false. |
| [isToolPreloadSupported](ToolingCapabilitiesMachineElement_isToolPreloadSupported.md) | If your machine has a staging function for the tool changer, set this to true. For machines without staging tool change capabilities, set this to false. |
| [isValid](ToolingCapabilitiesMachineElement_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxToolCount](ToolingCapabilitiesMachineElement_maxToolCount.md) | Property that represents the maximum number of tools available in the tool magazine, or the maximum number of tools that can be programmed in the control. |
| [objectType](ToolingCapabilitiesMachineElement_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [typeId](ToolingCapabilitiesMachineElement_typeId.md) | Identifier for this type of machine element. |

## Version

Introduced in version September 2025  

