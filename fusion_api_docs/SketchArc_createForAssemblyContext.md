# SketchArc.createForAssemblyContext Method

Parent Object: [SketchArc](SketchArc.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchArc_var" is a variable referencing a [SketchArc](SketchArc.md) object.

```python
returnValue = sketchArc_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

