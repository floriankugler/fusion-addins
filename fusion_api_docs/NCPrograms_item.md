# NCPrograms.item Method

Parent Object: [NCPrograms](NCPrograms.md)  

## Description

Function that returns the specified NC program using an index into the collection.

## Syntax

"nCPrograms_var" is a variable referencing a [NCPrograms](NCPrograms.md) object.

```python
returnValue = nCPrograms_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [NCProgram](NCProgram.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version April 2023  

