# MachineFromFileInput.create Method

Parent Object: [MachineFromFileInput](MachineFromFileInput.md)  

## Description

Creates a MachineFromFileInput object to be used as input for Machine.create method.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.MachineFromFileInput.create(filePath)
```

## Return Value

| Type | Description |
|----|----|
| [MachineFromFileInput](MachineFromFileInput.md) | The newly created "MachineFromFileInput" object in a valid state. |

## Parameters

| Name | Type | Description |
|----|----|----|
| filePath | string | The path to a machine file to be processed. The filePath is expected to be an absolute path to the machine file on disk. |

## Version

Introduced in version April 2023  

