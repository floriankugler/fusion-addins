# PrintSetting.syncWithMachine Method

Parent Object: [PrintSetting](PrintSetting.md)  

## Description

Synchronizes the print setting with the given machine, making extruder parameter options dependent on the available extruders in the machine.

## Syntax

"printSetting_var" is a variable referencing a [PrintSetting](PrintSetting.md) object.

```python
returnValue = printSetting_var.syncWithMachine(machine)
```

## Parameters

| Name    | Type                   | Description |
|---------|------------------------|-------------|
| machine | [Machine](Machine.md) |             |

## Version

Introduced in version March 2024  

