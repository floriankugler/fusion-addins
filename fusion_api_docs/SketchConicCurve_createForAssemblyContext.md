# SketchConicCurve.createForAssemblyContext Method

Parent Object: [SketchConicCurve](SketchConicCurve.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"sketchConicCurve_var" is a variable referencing a [SketchConicCurve](SketchConicCurve.md) object.

```python
returnValue = sketchConicCurve_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [SketchConicCurve](SketchConicCurve.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2015  

