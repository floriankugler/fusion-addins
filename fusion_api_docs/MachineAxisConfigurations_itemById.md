# MachineAxisConfigurations.itemById Method

Parent Object: [MachineAxisConfigurations](MachineAxisConfigurations.md)  

## Description

Get the configuration with the given ID

## Syntax

"machineAxisConfigurations_var" is a variable referencing a [MachineAxisConfigurations](MachineAxisConfigurations.md) object.

```python
returnValue = machineAxisConfigurations_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [MachineAxisConfiguration](MachineAxisConfiguration.md) | Return the MachineAxisConfiguration with the given ID, or null if the given ID does not match any configuration in the collection. |

## Parameters

| Name | Type   | Description                          |
|------|--------|--------------------------------------|
| id   | string | The ID for the configuration to get. |

## Version

Introduced in version April 2023  

