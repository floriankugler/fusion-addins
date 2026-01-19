# CircularPatternFeature.createForAssemblyContext Method

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"circularPatternFeature_var" is a variable referencing a [CircularPatternFeature](CircularPatternFeature.md) object.

```python
returnValue = circularPatternFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternFeature](CircularPatternFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2014  

