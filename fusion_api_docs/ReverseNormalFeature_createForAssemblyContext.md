# ReverseNormalFeature.createForAssemblyContext Method

Parent Object: [ReverseNormalFeature](ReverseNormalFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"reverseNormalFeature_var" is a variable referencing a [ReverseNormalFeature](ReverseNormalFeature.md) object.

```python
returnValue = reverseNormalFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ReverseNormalFeature](ReverseNormalFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version November 2015  

