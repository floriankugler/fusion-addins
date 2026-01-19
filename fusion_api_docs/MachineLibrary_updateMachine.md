# MachineLibrary.updateMachine Method

Parent Object: [MachineLibrary](MachineLibrary.md)  

## Description

Update a machine in the library. The library overrides the URL by given machine. Throws an error if the URL does not already point to an existing machine.

## Syntax

"machineLibrary_var" is a variable referencing a [MachineLibrary](MachineLibrary.md) object.

```python
returnValue = machineLibrary_var.updateMachine(url, machine)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if asset was updated successfully, false otherwise. |

## Parameters

| Name | Type | Description |
|----|----|----|
| url | [URL](URL.md) | The URL to the existing asset in the library that should be updated. |
| machine | [Machine](Machine.md) | The machine that should be persisted. |

## Version

Introduced in version April 2023  

