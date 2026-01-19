# Line3D.transformBy Method

Parent Object: [Line3D](Line3D.md)  

## Description

Transforms this curve in 3D space.

## Syntax

"line3D_var" is a variable referencing a [Line3D](Line3D.md) object.

```python
returnValue = line3D_var.transformBy(matrix)
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

