# SketchEllipticalArcs.item Method

Parent Object: [SketchEllipticalArcs](SketchEllipticalArcs.md)  

## Description

Function that returns the specified sketch elliptical arc using an index into the collection.

## Syntax

"sketchEllipticalArcs_var" is a variable referencing a [SketchEllipticalArcs](SketchEllipticalArcs.md) object.

```python
returnValue = sketchEllipticalArcs_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEllipticalArc](SketchEllipticalArc.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version August 2014  

