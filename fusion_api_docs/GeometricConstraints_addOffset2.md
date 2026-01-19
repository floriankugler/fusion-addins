# GeometricConstraints.addOffset2 Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates an offset constraint, which results in creating a new set of curves that are an offset of the input curves. The returned offset constraint object provides access to the created curves and the parameter controlling the offset.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addOffset2(input)
```

## Return Value

| Type | Description |
|----|----|
| [OffsetConstraint](OffsetConstraint.md) | Returns the newly created OffsetConstraint object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [OffsetConstraintInput](OffsetConstraintInput.md) | The OffsetConstraintInput object that defines the offset to create. |

## Version

Introduced in version September 2024  

