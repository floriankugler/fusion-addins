# OffsetConstraint.createForAssemblyContext Method

Parent Object: [OffsetConstraint](OffsetConstraint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"offsetConstraint_var" is a variable referencing an [OffsetConstraint](OffsetConstraint.md) object.

```python
returnValue = offsetConstraint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetConstraint](OffsetConstraint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version May 2016  

