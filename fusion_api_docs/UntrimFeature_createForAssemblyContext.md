# UntrimFeature.createForAssemblyContext Method

Parent Object: [UntrimFeature](UntrimFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"untrimFeature_var" is a variable referencing a [UntrimFeature](UntrimFeature.md) object.

```python
returnValue = untrimFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [UntrimFeature](UntrimFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2021  

