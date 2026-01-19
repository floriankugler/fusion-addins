# Matrix3D.setCell Method

Parent Object: [Matrix3D](Matrix3D.md)  

## Description

Sets the specified cell in the 4x4 matrix to the specified value.

## Syntax

"matrix3D_var" is a variable referencing a [Matrix3D](Matrix3D.md) object.

```python
returnValue = matrix3D_var.setCell(row, column, value)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name   | Type    | Description                                                 |
|--------|---------|-------------------------------------------------------------|
| row    | integer | The index of the row. The first row has in index of 0       |
| column | integer | The index of the column. The first column has an index of 0 |
| value  | double  | The new cell value.                                         |

## Version

Introduced in version August 2014  

