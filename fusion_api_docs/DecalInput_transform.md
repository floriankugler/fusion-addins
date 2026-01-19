# DecalInput.transform Property

Parent Object: [DecalInput](DecalInput.md)  

## Description

Gets and sets the transform of the decal. This controls the position, rotation, scaling, and flipping. This is done by providing a 3D matrix that defines a 3D coordinate system in model space. The origin of the matrix defines the center of the decal and must lie somewhere on the first face. The Z-axis of the matrix should be the same as the normal of the face at the origin. The X and Y axes define the orientation of the decal and must be both perpendicular to the Z and each other. Reversing the direction of the X or Y axis will flip the decal in that direction. The magnitude of the X and Y axes controls the scale, and the scale can be non-uniform, meaning the length of the X and Y vectors do not need to be the same.

## Syntax

"decalInput_var" is a variable referencing a DecalInput object.  

```python
# Get the value of the property.
propertyValue = decalInput_var.transform

# Set the value of the property.
decalInput_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version September 2024  

