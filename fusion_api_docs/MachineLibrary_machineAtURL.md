# MachineLibrary.machineAtURL Method

Parent Object: [MachineLibrary](MachineLibrary.md)  

## Description

Get a specific machine by the given URL. Returns null, if the URL does not exist.

## Syntax

"machineLibrary_var" is a variable referencing a [MachineLibrary](MachineLibrary.md) object.

```python
returnValue = machineLibrary_var.machineAtURL(url)
```

## Return Value

| Type | Description |
|----|----|
| [Machine](Machine.md) | Returns the machine for a valid URL, returns null otherwise. |

## Parameters

| Name | Type           | Description                          |
|------|----------------|--------------------------------------|
| url  | [URL](URL.md) | The URL to the machine to be loaded. |

## Version

Introduced in version April 2023  

