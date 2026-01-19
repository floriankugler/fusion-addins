# SketchEntityList.item Method

Parent Object: [SketchEntityList](SketchEntityList.md)  

## Description

Function that returns the specified sketch entity using an index into the collection.

## Syntax

"sketchEntityList_var" is a variable referencing a [SketchEntityList](SketchEntityList.md) object.

```python
returnValue = sketchEntityList_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEntity](SketchEntity.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version June 2015  

