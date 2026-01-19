# Surface.transformBy Method

Parent Object: [Surface](Surface.md)  

## Description

Updates this surface by transforming it with a given input matrix.

## Syntax

"surface_var" is a variable referencing a [Surface](Surface.md) object.

```python
returnValue = surface_var.transformBy(matrix)
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

