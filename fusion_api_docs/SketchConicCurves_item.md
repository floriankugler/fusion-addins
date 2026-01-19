# SketchConicCurves.item Method

Parent Object: [SketchConicCurves](SketchConicCurves.md)  

## Description

Function that returns the specified conic curve using an index into the collection.

## Syntax

"sketchConicCurves_var" is a variable referencing a [SketchConicCurves](SketchConicCurves.md) object.

```python
returnValue = sketchConicCurves_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchConicCurve](SketchConicCurve.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2015  

