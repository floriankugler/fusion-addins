# StitchFeature.createForAssemblyContext Method

Parent Object: [StitchFeature](StitchFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"stitchFeature_var" is a variable referencing a [StitchFeature](StitchFeature.md) object.

```python
returnValue = stitchFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [StitchFeature](StitchFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version June 2015  

