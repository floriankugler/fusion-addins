# SketchCircle.createForAssemblyContext Method

Parent Object: [SketchCircle](SketchCircle.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchCircle_var" is a variable referencing a [SketchCircle](SketchCircle.md) object.

```python
returnValue = sketchCircle_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchCircle](SketchCircle.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

