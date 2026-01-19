# NurbsCurve3D.transformBy Method

Parent Object: [NurbsCurve3D](NurbsCurve3D.md)  

## Description

Transforms this curve in 3D space.

## Syntax

"nurbsCurve3D_var" is a variable referencing a [NurbsCurve3D](NurbsCurve3D.md) object.

```python
returnValue = nurbsCurve3D_var.transformBy(matrix)
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Return true if the transform was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| matrix | [Matrix3D](Matrix3D.md) | A 3D matrix that defines the transform to apply to the curve. |

## Version

Introduced in version August 2014  

