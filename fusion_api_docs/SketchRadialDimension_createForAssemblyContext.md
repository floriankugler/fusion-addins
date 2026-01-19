# SketchRadialDimension.createForAssemblyContext Method

Parent Object: [SketchRadialDimension](SketchRadialDimension.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchRadialDimension_var" is a variable referencing a [SketchRadialDimension](SketchRadialDimension.md) object.

```python
returnValue = sketchRadialDimension_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchRadialDimension](SketchRadialDimension.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

