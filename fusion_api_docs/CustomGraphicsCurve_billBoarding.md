# CustomGraphicsCurve.billBoarding Property

Parent Object: [CustomGraphicsCurve](CustomGraphicsCurve.md)  

## Description

Gets and sets the billboarding behavior of this custom graphics entity. To define billboarding you can set this property using a CustomGraphicsBillBoard objects that you statically create using the create method of the CustomGraphicsBillBoard class. To remove billboarding from this entity you can set this property to null.  

Billboarding is used to specify that the orientation of custom graphics is defined relative to the screen instead of model space. This is commonly used for legends and symbols that you want to always face the user, even as the camera is rotated.

## Syntax

"customGraphicsCurve_var" is a variable referencing a CustomGraphicsCurve object.  

```python
# Get the value of the property.
propertyValue = customGraphicsCurve_var.billBoarding

# Set the value of the property.
customGraphicsCurve_var.billBoarding = propertyValue
```

## Property Value

This is a read/write property whose value is a [CustomGraphicsBillBoard](CustomGraphicsBillBoard.md).

## Version

Introduced in version September 2017  

