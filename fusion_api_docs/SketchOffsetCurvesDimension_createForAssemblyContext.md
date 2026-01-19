# SketchOffsetCurvesDimension.createForAssemblyContext Method

Parent Object: [SketchOffsetCurvesDimension](SketchOffsetCurvesDimension.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchOffsetCurvesDimension_var" is a variable referencing a [SketchOffsetCurvesDimension](SketchOffsetCurvesDimension.md) object.

```python
returnValue = sketchOffsetCurvesDimension_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchOffsetCurvesDimension](SketchOffsetCurvesDimension.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version May 2016  

