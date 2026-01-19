# Matrix3D.setToRotateTo Method

Parent Object: [Matrix3D](Matrix3D.md)  

## Description

Sets to the matrix of rotation that would align the 'from' vector with the 'to' vector. The optional axis argument may be used when the two vectors are perpendicular and in opposite directions to specify a specific solution, but is otherwise ignored

## Syntax

"matrix3D_var" is a variable referencing a [Matrix3D](Matrix3D.md) object.

```python
# Uses no optional arguments.
returnValue = matrix3D_var.setToRotateTo(from, to)

# Uses optional arguments.
returnValue = matrix3D_var.setToRotateTo(from, to, axis)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| from | [Vector3D](Vector3D.md) | The vector to rotate from. |
| to | [Vector3D](Vector3D.md) | The vector to rotate to. |
| axis | [Vector3D](Vector3D.md) | The optional axis vector to disambiguate the rotation axis. This is an optional argument whose default value is null. |

## Version

Introduced in version August 2014  

