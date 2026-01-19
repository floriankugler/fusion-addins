# Machine.create Method

Parent Object: [Machine](Machine.md)  

## Description

Creates a machine from a "MachineInput" input object

## Remarks

"MachineFromFileInput" and "MachineFromLibraryInput" can be used to create valid input objects.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.Machine.create(machineInput)
```

## Return Value

| Type | Description |
|----|----|
| [Machine](Machine.md) | Returns the newly created machine in a valid state. |

## Parameters

| Name | Type | Description |
|----|----|----|
| machineInput | [MachineInput](MachineInput.md) | Input object that is used to hold the details needed for creating a machine. |

## Version

Introduced in version April 2023  

