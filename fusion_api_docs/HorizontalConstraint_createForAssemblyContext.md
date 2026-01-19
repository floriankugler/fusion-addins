# HorizontalConstraint.createForAssemblyContext Method

Parent Object: [HorizontalConstraint](HorizontalConstraint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"horizontalConstraint_var" is a variable referencing a [HorizontalConstraint](HorizontalConstraint.md) object.

```python
returnValue = horizontalConstraint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [HorizontalConstraint](HorizontalConstraint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

