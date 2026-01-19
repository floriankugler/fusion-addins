# FilletEdgeSetInputs.item Method

Parent Object: [FilletEdgeSetInputs](FilletEdgeSetInputs.md)  

## Description

Function that returns the specified fillet edge set input using an index into the collection.

## Syntax

"filletEdgeSetInputs_var" is a variable referencing a [FilletEdgeSetInputs](FilletEdgeSetInputs.md) object.

```python
returnValue = filletEdgeSetInputs_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [FilletEdgeSetInput](FilletEdgeSetInput.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. The edge sets are returned in the same order they were created in. |

## Version

Introduced in version November 2022  

