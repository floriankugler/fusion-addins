# SketchPoints.item Method

Parent Object: [SketchPoints](SketchPoints.md)  

## Description

Function that returns the specified sketch using an index into the collection.

## Syntax

"sketchPoints_var" is a variable referencing a [SketchPoints](SketchPoints.md) object.

```python
returnValue = sketchPoints_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchPoint](SketchPoint.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

