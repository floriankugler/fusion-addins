# OffsetFacesFeatureInput.distance Property

Parent Object: [OffsetFacesFeatureInput](OffsetFacesFeatureInput.md)  

## Description

The distance of the offset. A positive value offsets the faces in the direction of the face normal. A negative value goes in the other direction.  

This is a ValueInput object that can be created using either createByReal or createByString. When a real ValueInput is used, the value is centimeters. When a string ValueInput is used, it defines the expression of the parameter that will be created to control the feature and any valid expression that defines a distance can be used.

## Syntax

"offsetFacesFeatureInput_var" is a variable referencing an OffsetFacesFeatureInput object.  

```python
# Get the value of the property.
propertyValue = offsetFacesFeatureInput_var.distance

# Set the value of the property.
offsetFacesFeatureInput_var.distance = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2025  

