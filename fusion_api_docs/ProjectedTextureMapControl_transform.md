# ProjectedTextureMapControl.transform Property

Parent Object: [ProjectedTextureMapControl](ProjectedTextureMapControl.md)  

## Description

Gets and sets the transform that defines the position and orientation of how the texture is projected onto the body. The Z axis of the transform corresponds to the axis that is specified in the user-interface and is the primary direction of the texture.

## Syntax

"projectedTextureMapControl_var" is a variable referencing a ProjectedTextureMapControl object.  

```python
# Get the value of the property.
propertyValue = projectedTextureMapControl_var.transform

# Set the value of the property.
projectedTextureMapControl_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version March 2022  

