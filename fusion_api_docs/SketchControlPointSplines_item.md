# SketchControlPointSplines.item Method

Parent Object: [SketchControlPointSplines](SketchControlPointSplines.md)  

## Description

Function that returns the specified sketch control point spline using an index into the collection.

## Syntax

"sketchControlPointSplines_var" is a variable referencing a [SketchControlPointSplines](SketchControlPointSplines.md) object.

```python
returnValue = sketchControlPointSplines_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchControlPointSpline](SketchControlPointSpline.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version July 2022  

