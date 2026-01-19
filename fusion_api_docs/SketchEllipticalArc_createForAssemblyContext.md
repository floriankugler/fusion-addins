# SketchEllipticalArc.createForAssemblyContext Method

Parent Object: [SketchEllipticalArc](SketchEllipticalArc.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchEllipticalArc_var" is a variable referencing a [SketchEllipticalArc](SketchEllipticalArc.md) object.

```python
returnValue = sketchEllipticalArc_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEllipticalArc](SketchEllipticalArc.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

