# ExtendFeature.createForAssemblyContext Method

Parent Object: [ExtendFeature](ExtendFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"extendFeature_var" is a variable referencing an [ExtendFeature](ExtendFeature.md) object.

```python
returnValue = extendFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ExtendFeature](ExtendFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version June 2015  

