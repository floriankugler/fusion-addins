# MachinePartInput.createAxisInput Method

Parent Object: [MachinePartInput](MachinePartInput.md)  

## Description

Creates a new MachineAxisInput object to be used to create a new MachineAxis. Set this object on to an axis type MachinePartInput to create a new MachineAxis with that part.

## Syntax

"machinePartInput_var" is a variable referencing a [MachinePartInput](MachinePartInput.md) object.

```python
returnValue = machinePartInput_var.createAxisInput(axisType)
```

## Return Value

| Type | Description |
|----|----|
| [MachineAxisInput](MachineAxisInput.md) | Returns a LinearMachineAxisInput or RotaryMachineAxisInput, or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| axisType | [MachineAxisTypes](MachineAxisTypes.md) | The type of MachineAxisInput to create. |

## Version

Introduced in version April 2023  

