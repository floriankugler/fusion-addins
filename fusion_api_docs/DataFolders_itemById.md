# DataFolders.itemById Method

Parent Object: [DataFolders](DataFolders.md)  

## Description

Returns the folder specified using the ID of the folder.

## Syntax

"dataFolders_var" is a variable referencing a [DataFolders](DataFolders.md) object.

```python
returnValue = dataFolders_var.itemById(id)
```

## Return Value

| Type | Description |
|----|----|
| [DataFolder](DataFolder.md) | Returns the folder or null if a folder with the specified ID is not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| id | string | The ID of the folder to return. This is the same ID used by the APS Data Management API. |

## Version

Introduced in version September 2016  

