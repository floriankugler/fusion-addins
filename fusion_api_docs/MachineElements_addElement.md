# MachineElements.addElement Method

Parent Object: [MachineElements](MachineElements.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Add a new machine element to the machine.

## Syntax

"machineElements_var" is a variable referencing a [MachineElements](MachineElements.md) object.

```python
returnValue = machineElements_var.addElement(input)
```

## Return Value

| Type                                 | Description                |
|--------------------------------------|----------------------------|
| [MachineElement](MachineElement.md) | The created MachineElement |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MachineElementInput](MachineElementInput.md) | A specialization of MachineElementInput class that contains the properties required to create a new machine element. |

## Version

Introduced in version September 2025  

