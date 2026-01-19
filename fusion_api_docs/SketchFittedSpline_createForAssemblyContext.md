# SketchFittedSpline.createForAssemblyContext Method

Parent Object: [SketchFittedSpline](SketchFittedSpline.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchFittedSpline_var" is a variable referencing a [SketchFittedSpline](SketchFittedSpline.md) object.

```python
returnValue = sketchFittedSpline_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchFittedSpline](SketchFittedSpline.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

