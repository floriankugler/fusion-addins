# Decal.transform Property

Parent Object: [Decal](Decal.md)  

## Description

Gets the transform of the decal. The returned matrix defines the position, rotation, scaling, and flipping. This is done by providing a 3D matrix which defines a 3D coordinate system in model space. The origin of the matrix defines the center of the decal and must lie somewhere on the first face. The normal of the face defines the Z axis of the matrix and the X and Y axes define the orientation of the decal and must be both perpendicular to the Z axis and to each other. Reversing the direction of the X or Y axis will flip the decal in that direction. The magnitude of the X and Y axes controls the scale and the scale can be non-uniform, meaning the length of the X and Y vectors do not need to be the same.  

To set the transform, use the redefine method.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.transform
```

## Property Value

This is a read only property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version September 2024  

