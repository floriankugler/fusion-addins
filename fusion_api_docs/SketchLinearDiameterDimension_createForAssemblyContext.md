# SketchLinearDiameterDimension.createForAssemblyContext Method

Parent Object: [SketchLinearDiameterDimension](SketchLinearDiameterDimension.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchLinearDiameterDimension_var" is a variable referencing a [SketchLinearDiameterDimension](SketchLinearDiameterDimension.md) object.

```python
returnValue = sketchLinearDiameterDimension_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchLinearDiameterDimension](SketchLinearDiameterDimension.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2022  

