# SketchText.createForAssemblyContext Method

Parent Object: [SketchText](SketchText.md)  

## Description

Creates a proxy object for the SketchText object that represents the SketchText object in the context of an assembly. The context is defined by the input occurrence.

## Syntax

"sketchText_var" is a variable referencing a [SketchText](SketchText.md) object.

```python
returnValue = sketchText_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchText](SketchText.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version May 2022  

