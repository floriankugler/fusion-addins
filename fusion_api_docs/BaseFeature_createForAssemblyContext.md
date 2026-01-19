# BaseFeature.createForAssemblyContext Method

Parent Object: [BaseFeature](BaseFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"baseFeature_var" is a variable referencing a [BaseFeature](BaseFeature.md) object.

```python
returnValue = baseFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [BaseFeature](BaseFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version January 2021  

