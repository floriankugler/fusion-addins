# ProfileCurves.item Method

Parent Object: [ProfileCurves](ProfileCurves.md)  

## Description

Function that returns the specified profile curve using an index into the collection.

## Syntax

"profileCurves_var" is a variable referencing a [ProfileCurves](ProfileCurves.md) object.

```python
returnValue = profileCurves_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [ProfileCurve](ProfileCurve.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

