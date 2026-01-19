# MachineFromLibraryInput.create Method

Parent Object: [MachineFromLibraryInput](MachineFromLibraryInput.md)  

## Description

Creates a MachineFromLibraryInput object to be used as input for Machine.create method, in order to create a machine from a library location.

## Syntax

This is a static method.  

```python

returnValue = adsk.cam.MachineFromLibraryInput.create(url)
```

## Return Value

| Type | Description |
|----|----|
| [MachineFromLibraryInput](MachineFromLibraryInput.md) | Returns newly created MachineFromLibraryInput object in a valid state. |

## Parameters

| Name | Type           | Description                          |
|------|----------------|--------------------------------------|
| url  | [URL](URL.md) | The URL path to the library machine. |

## Version

Introduced in version April 2023  

