# ProjectedTextureMapControl.isCapped Property

Parent Object: [ProjectedTextureMapControl](ProjectedTextureMapControl.md)  

## Description

When a cylindrical projected texture map is being used this property gets and sets if a cap is use for the cylindrical projection. This property is only valid in the case when the projectedTextureMapType returns CylindricalTextureMapProjection. The value of this property should be ignored in all other cases and setting the property will have no effect.

## Syntax

"projectedTextureMapControl_var" is a variable referencing a ProjectedTextureMapControl object.  

```python
# Get the value of the property.
propertyValue = projectedTextureMapControl_var.isCapped

# Set the value of the property.
projectedTextureMapControl_var.isCapped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version March 2022  

