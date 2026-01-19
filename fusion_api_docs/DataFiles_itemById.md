# DataFiles.itemById Method

Parent Object: [DataFiles](DataFiles.md)  

## Description

Returns the file specified using the ID or version ID of the file.

## Syntax

"dataFiles_var" is a variable referencing a [DataFiles](DataFiles.md) object.

```python
returnValue = dataFiles_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [DataFile](DataFile.md) | Returns the file or null if a file with the specified ID is not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID or version ID of the file to return. This is the same ID used by the APS Data Management API. |

## Version

Introduced in version December 2020  

