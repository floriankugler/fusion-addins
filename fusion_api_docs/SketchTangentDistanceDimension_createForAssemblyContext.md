# SketchTangentDistanceDimension.createForAssemblyContext Method

Parent Object: [SketchTangentDistanceDimension](SketchTangentDistanceDimension.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchTangentDistanceDimension_var" is a variable referencing a [SketchTangentDistanceDimension](SketchTangentDistanceDimension.md) object.

```python
returnValue = sketchTangentDistanceDimension_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchTangentDistanceDimension](SketchTangentDistanceDimension.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version July 2022  

