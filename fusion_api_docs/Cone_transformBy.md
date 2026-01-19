# Cone.transformBy Method

Parent Object: [Cone](Cone.md)  

## Description

Updates this surface by transforming it with a given input matrix.

## Syntax

"cone_var" is a variable referencing a [Cone](Cone.md) object.

```python
returnValue = cone_var.transformBy(matrix)
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

