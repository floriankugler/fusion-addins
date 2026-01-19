# SketchArcs.item Method

Parent Object: [SketchArcs](SketchArcs.md)  

## Description

Function that returns the specified sketch arc using an index into the collection.

## Syntax

"sketchArcs_var" is a variable referencing a [SketchArcs](SketchArcs.md) object.

```python
returnValue = sketchArcs_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

