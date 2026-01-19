# MachineElements.createMachineElementInput Method

Parent Object: [MachineElements](MachineElements.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Create a new MachineElementInput object for the specified type. This is intedned to be used to create/add new machine elements.

## Syntax

"machineElements_var" is a variable referencing a [MachineElements](MachineElements.md) object.

```python
returnValue = machineElements_var.createMachineElementInput(type)
```

## Return Value

| Type | Description |
|----|----|
| [MachineElementInput](MachineElementInput.md) | A MachineElementInput object |

## Parameters

| Name | Type | Description |
|----|----|----|
| type | [MachineElementInputType](MachineElementInputType.md) | The type of machine element to create the input for |

## Version

Introduced in version September 2025  

