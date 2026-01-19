# SketchTexts.item Method

Parent Object: [SketchTexts](SketchTexts.md)  

## Description

Function that returns the specified sketch text using an index into the collection.

## Syntax

"sketchTexts_var" is a variable referencing a [SketchTexts](SketchTexts.md) object.

```python
returnValue = sketchTexts_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [SketchText](SketchText.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version March 2015  

