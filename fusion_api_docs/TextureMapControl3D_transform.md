# TextureMapControl3D.transform Property

Parent Object: [TextureMapControl3D](TextureMapControl3D.md)  

## Description

Gets and sets the transform that defines the position and orientation of how the texture is applied to the body. For wood grain, the Z direction of the defined coordinate system is the direction of the grain.

## Syntax

"textureMapControl3D_var" is a variable referencing a TextureMapControl3D object.  

```python
# Get the value of the property.
propertyValue = textureMapControl3D_var.transform

# Set the value of the property.
textureMapControl3D_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version March 2022  

