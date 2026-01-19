# ArrangeFeature.createForAssemblyContext Method

Parent Object: [ArrangeFeature](ArrangeFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"arrangeFeature_var" is a variable referencing an [ArrangeFeature](ArrangeFeature.md) object.

```python
returnValue = arrangeFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ArrangeFeature](ArrangeFeature.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2025  

