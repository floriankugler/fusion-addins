# SketchCircles.item Method

Parent Object: [SketchCircles](SketchCircles.md)  

## Description

Function that returns the specified sketch circle using an index into the collection.

## Syntax

"sketchCircles_var" is a variable referencing a [SketchCircles](SketchCircles.md) object.

```python
returnValue = sketchCircles_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

