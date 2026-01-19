# RevolveFeature.createForAssemblyContext Method

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"revolveFeature_var" is a variable referencing a [RevolveFeature](RevolveFeature.md) object.

```python
returnValue = revolveFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [RevolveFeature](RevolveFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

