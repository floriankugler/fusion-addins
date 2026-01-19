# DataFolders.add Method

Parent Object: [DataFolders](DataFolders.md)  

## Description

Creates a new folder within the parent folder.

## Syntax

"dataFolders_var" is a variable referencing a [DataFolders](DataFolders.md) object.

```python
returnValue = dataFolders_var.add(name)
```

## Return Value

| Type | Description |
|----|----|
| [DataFolder](DataFolder.md) | Returns the created DataFolder or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the folder. This must be unique with respect to the other folders within the parent folder. |

## Version

Introduced in version September 2016  

