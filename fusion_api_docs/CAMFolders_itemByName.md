# CAMFolders.itemByName Method

Parent Object: [CAMFolders](CAMFolders.md)  

## Description

Returns the folder with the specified name (as appears in the browser).

## Syntax

"cAMFolders_var" is a variable referencing a [CAMFolders](CAMFolders.md) object.

```python
returnValue = cAMFolders_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [CAMFolder](CAMFolder.md) | Returns the specified folder or null in the case where there is no folder with the specified name. |

## Parameters

| Name | Type   | Description                                            |
|------|--------|--------------------------------------------------------|
| name | string | The name (as it appears in the browser) of the folder. |

## Version

Introduced in version January 2016  

