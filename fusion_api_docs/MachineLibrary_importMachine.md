# MachineLibrary.importMachine Method

Parent Object: [MachineLibrary](MachineLibrary.md)  

## Description

Import a given machine at a specific location. The machine will be stored in the library. Throws an error, if the given URL is read-only.

## Syntax

"machineLibrary_var" is a variable referencing a [MachineLibrary](MachineLibrary.md) object.

```python
returnValue = machineLibrary_var.importMachine(machine, destinationUrl, machineName)
```

## Return Value

| Type | Description |
|----|----|
| [URL](URL.md) | Returns the URL of the newly imported machine, or null if the import failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| machine | [Machine](Machine.md) | The machine that should be imported. |
| destinationUrl | [URL](URL.md) | The URL to the folder where to save the machine. |
| machineName | string | The name of the machine that should be created due to the import. The name can be extended if the asset already exists at given location to ensure a unique name. |

## Version

Introduced in version April 2023  

