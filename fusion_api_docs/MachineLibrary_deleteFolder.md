# MachineLibrary.deleteFolder Method

Parent Object: [MachineLibrary](MachineLibrary.md)  

## Description

Delete folder by URL from the library. Any content of the folder will also be deleted. Throw an error if given URL does not point to a valid folder or the URL is read-only.

## Syntax

"machineLibrary_var" is a variable referencing a [MachineLibrary](MachineLibrary.md) object.

```python
returnValue = machineLibrary_var.deleteFolder(url)
```

## Return Value

| Type    | Description                                                      |
|---------|------------------------------------------------------------------|
| boolean | Returns true if folder was deleted successfully, false otherwise |

## Parameters

| Name | Type           | Description                                   |
|------|----------------|-----------------------------------------------|
| url  | [URL](URL.md) | The URL to the folder that should be removed. |

## Version

Introduced in version April 2023  

