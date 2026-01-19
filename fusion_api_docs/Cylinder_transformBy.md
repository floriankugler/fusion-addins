# Cylinder.transformBy Method

Parent Object: [Cylinder](Cylinder.md)  

## Description

Updates this surface by transforming it with a given input matrix.

## Syntax

"cylinder_var" is a variable referencing a [Cylinder](Cylinder.md) object.

```python
returnValue = cylinder_var.transformBy(matrix)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the transform was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| matrix | [Matrix3D](Matrix3D.md) | A 3D matrix that defines the transform to apply to the surface. |

## Version

Introduced in version August 2014  

