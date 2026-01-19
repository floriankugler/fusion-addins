# RevolveFeatureInput.axis Property

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Gets and sets the entity used to define the axis of revolution. The axis can be a sketch line, construction axis, linear edge or a face that defines an axis (cylinder, cone, torus, etc.). If it is not in the same plane as the profile, it is projected onto the profile plane.

## Syntax

"revolveFeatureInput_var" is a variable referencing a RevolveFeatureInput object.  

```python
# Get the value of the property.
propertyValue = revolveFeatureInput_var.axis

# Set the value of the property.
revolveFeatureInput_var.axis = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

