# ThickenFeature.createForAssemblyContext Method

Parent Object: [ThickenFeature](ThickenFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"thickenFeature_var" is a variable referencing a [ThickenFeature](ThickenFeature.md) object.

```python
returnValue = thickenFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [ThickenFeature](ThickenFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version June 2015  

