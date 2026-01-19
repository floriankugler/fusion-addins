# Decal.createForAssemblyContext Method

Parent Object: [Decal](Decal.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"decal_var" is a variable referencing a [Decal](Decal.md) object.

```python
returnValue = decal_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [Decal](Decal.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2024  

