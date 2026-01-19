# VerticalPointsConstraint.createForAssemblyContext Method

Parent Object: [VerticalPointsConstraint](VerticalPointsConstraint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"verticalPointsConstraint_var" is a variable referencing a [VerticalPointsConstraint](VerticalPointsConstraint.md) object.

```python
returnValue = verticalPointsConstraint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [VerticalPointsConstraint](VerticalPointsConstraint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version August 2014  

