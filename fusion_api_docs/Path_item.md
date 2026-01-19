# Path.item Method

Parent Object: [Path](Path.md)  

## Description

Function that returns the specified PathEntity using an index into the collection.

## Syntax

"path_var" is a variable referencing a [Path](Path.md) object.

```python
returnValue = path_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [PathEntity](PathEntity.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version November 2014  

