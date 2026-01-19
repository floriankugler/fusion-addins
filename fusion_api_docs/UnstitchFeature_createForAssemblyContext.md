# UnstitchFeature.createForAssemblyContext Method

Parent Object: [UnstitchFeature](UnstitchFeature.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"unstitchFeature_var" is a variable referencing a [UnstitchFeature](UnstitchFeature.md) object.

```python
returnValue = unstitchFeature_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [UnstitchFeature](UnstitchFeature.md) | Returns the proxy object or null if this is not the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version July 2015  

