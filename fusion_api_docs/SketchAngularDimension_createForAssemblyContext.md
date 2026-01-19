# SketchAngularDimension.createForAssemblyContext Method

Parent Object: [SketchAngularDimension](SketchAngularDimension.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchAngularDimension_var" is a variable referencing a [SketchAngularDimension](SketchAngularDimension.md) object.

```python
returnValue = sketchAngularDimension_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchAngularDimension](SketchAngularDimension.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

