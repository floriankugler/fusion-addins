# CustomGraphicsCurve.curve Property

Parent Object: [CustomGraphicsCurve](CustomGraphicsCurve.md)  

## Description

Gets and sets the curve associated with this graphics entity. Any of the curve types derived from Curve3D is valid except for InfiniteLine3D.

## Syntax

"customGraphicsCurve_var" is a variable referencing a CustomGraphicsCurve object.  

```python
# Get the value of the property.
propertyValue = customGraphicsCurve_var.curve

# Set the value of the property.
customGraphicsCurve_var.curve = propertyValue
```

## Property Value

This is a read/write property whose value is a [Curve3D](Curve3D.md).

## Version

Introduced in version September 2017  

