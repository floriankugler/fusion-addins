# SketchLineList.item Method

Parent Object: [SketchLineList](SketchLineList.md)  

## Description

Function that returns the specified sketch line using an index into the collection.

## Syntax

"sketchLineList_var" is a variable referencing a [SketchLineList](SketchLineList.md) object.

```python
returnValue = sketchLineList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLine](SketchLine.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

