# SketchCurves.item Method

Parent Object: [SketchCurves](SketchCurves.md)  

## Description

Function that returns the specified sketch curve using an index into the collection.

## Syntax

"sketchCurves_var" is a variable referencing a [SketchCurves](SketchCurves.md) object.

```python
returnValue = sketchCurves_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCurve](SketchCurve.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

