# MachineLibrary.childFolderURLs Method

Parent Object: [MachineLibrary](MachineLibrary.md)  

## Description

Get all library folders under given URL.

## Syntax

"machineLibrary_var" is a variable referencing a [MachineLibrary](MachineLibrary.md) object.

```python
returnValue = machineLibrary_var.childFolderURLs(url)
```

## Return Value

| Type               | Description                                    |
|--------------------|------------------------------------------------|
| [URL](URL.md)\[\] | Returns list of folder URLs at given location. |

## Parameters

| Name | Type           | Description                   |
|------|----------------|-------------------------------|
| url  | [URL](URL.md) | The URL to the parent folder. |

## Version

Introduced in version April 2023  

