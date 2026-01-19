# DataFiles.item Method

Parent Object: [DataFiles](DataFiles.md)  

## Description

Returns the specified data file.

## Syntax

"dataFiles_var" is a variable referencing a [DataFiles](DataFiles.md) object.

```python
returnValue = dataFiles_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [DataFile](DataFile.md) | Returns the specified file or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the file to return. The first file in the list has an index of 0. |

## Version

Introduced in version January 2015  

