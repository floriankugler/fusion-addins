# Setup.workCoordinateSystem Property

Parent Object: [Setup](Setup.md)  

## Description

Gets the Work Coordinate System associated with the setup as 4x4 matrix. From Matrix3D, Orientation and Origin data can be fetched.

## Syntax

"setup_var" is a variable referencing a Setup object.  

```python
# Get the value of the property.
propertyValue = setup_var.workCoordinateSystem
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version April 2023  

