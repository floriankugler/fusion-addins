# RectangularPatternFeature.createForAssemblyContext Method

Parent Object: [RectangularPatternFeature](RectangularPatternFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"rectangularPatternFeature_var" is a variable referencing a [RectangularPatternFeature](RectangularPatternFeature.md) object.

```python
returnValue = rectangularPatternFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [RectangularPatternFeature](RectangularPatternFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2014  

