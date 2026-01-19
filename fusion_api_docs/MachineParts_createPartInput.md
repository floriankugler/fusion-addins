# MachineParts.createPartInput Method

Parent Object: [MachineParts](MachineParts.md)  

## Description

Create a new MachinePartInput.

## Syntax

"machineParts_var" is a variable referencing a [MachineParts](MachineParts.md) object.

```python
returnValue = machineParts_var.createPartInput(partType)
```

## Return Value

| Type | Description |
|----|----|
| [MachinePartInput](MachinePartInput.md) | Returns the new MachinePartInput or null if creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| partType | [MachinePartTypes](MachinePartTypes.md) | The type of part to create. When this parameter is Axis, you must set a value for axisInput. |

## Version

Introduced in version April 2023  

