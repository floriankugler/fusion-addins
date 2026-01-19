# MachineAxisConfigurations.addLinear Method

Parent Object: [MachineAxisConfigurations](MachineAxisConfigurations.md)  

## Description

Add a new linear axis configuration for a kinematics part.

## Syntax

"machineAxisConfigurations_var" is a variable referencing a [MachineAxisConfigurations](MachineAxisConfigurations.md) object.

```python
returnValue = machineAxisConfigurations_var.addLinear(partId)
```

## Return Value

| Type | Description |
|----|----|
| [LinearMachineAxisConfiguration](LinearMachineAxisConfiguration.md) | Returns the newly created LinearMachineAxisConfiguration or null if creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| partId | string | ID used to label this axis configuration and link to a part in the kinematics tree. partID must match a part of type AxisMachinePartType in the kinematics tree and the part must be a linear axis. |

## Version

Introduced in version April 2023  

