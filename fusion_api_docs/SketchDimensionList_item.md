# SketchDimensionList.item Method

Parent Object: [SketchDimensionList](SketchDimensionList.md)  

## Description

Function that returns the specified sketch dimension using an index into the collection.

## Syntax

"sketchDimensionList_var" is a variable referencing a [SketchDimensionList](SketchDimensionList.md) object.

```python
returnValue = sketchDimensionList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchDimension](SketchDimension.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

