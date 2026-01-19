# CAMFolders.itemByOperationId Method

Parent Object: [CAMFolders](CAMFolders.md)  

## Description

Returns the folder with the specified operation id.

## Syntax

"cAMFolders_var" is a variable referencing a [CAMFolders](CAMFolders.md) object.

```python
returnValue = cAMFolders_var.itemByOperationId(id)
```

## Return Value

| Type | Description |
|----|----|
| [CAMFolder](CAMFolder.md) | Returns the specified folder or null in the case where there is no folder with the specified operation id. |

## Parameters

| Name | Type    | Description           |
|------|---------|-----------------------|
| id   | integer | The id of the folder. |

## Version

Introduced in version May 2020  

