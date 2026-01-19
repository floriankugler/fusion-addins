# SketchFixedSplines.item Method

Parent Object: [SketchFixedSplines](SketchFixedSplines.md)  

## Description

Function that returns the specified sketch fixed spline using an index into the collection.

## Syntax

"sketchFixedSplines_var" is a variable referencing a [SketchFixedSplines](SketchFixedSplines.md) object.

```python
returnValue = sketchFixedSplines_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchFixedSpline](SketchFixedSpline.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

