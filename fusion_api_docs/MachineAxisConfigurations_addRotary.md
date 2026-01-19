# MachineAxisConfigurations.addRotary Method

Parent Object: [MachineAxisConfigurations](MachineAxisConfigurations.md)  

## Description

Add a new rotary axis configuration for a kinematics part.

## Syntax

"machineAxisConfigurations_var" is a variable referencing a [MachineAxisConfigurations](MachineAxisConfigurations.md) object.

```python
returnValue = machineAxisConfigurations_var.addRotary(partId)
```

## Return Value

| Type | Description |
|----|----|
| [RotaryMachineAxisConfiguration](RotaryMachineAxisConfiguration.md) | Returns the newly created RotaryMachineAxisConfiguration or null if creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| partId | string | ID used to label this axis configuration and link to a part in the kinematics tree. partID must match a part of type AxisMachinePartType in the kinematics tree and the part must be a rotary axis. |

## Version

Introduced in version April 2023  

