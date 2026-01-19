# RectangularPatternConstraint.createForAssemblyContext Method

Parent Object: [RectangularPatternConstraint](RectangularPatternConstraint.md)  

## Description

Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence.

## Syntax

"rectangularPatternConstraint_var" is a variable referencing a [RectangularPatternConstraint](RectangularPatternConstraint.md) object.

```python
returnValue = rectangularPatternConstraint_var.createForAssemblyContext(occurrence)
```

## Return Value

| Type | Description |
|----|----|
| [RectangularPatternConstraint](RectangularPatternConstraint.md) | Returns the proxy object or null if this isn't the NativeObject. |

## Parameters

| Name | Type | Description |
|----|----|----|
| occurrence | [Occurrence](Occurrence.md) | The occurrence that defines the context to create the proxy in. |

## Version

Introduced in version September 2022  

