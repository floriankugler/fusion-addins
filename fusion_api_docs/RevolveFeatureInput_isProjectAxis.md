# RevolveFeatureInput.isProjectAxis Property

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Specifies if the axis should be projected on the same plane as the profile sketch plane or not.  

Setting this to true will use a projected axis, while setting it to false will keep it in its original location. This is initialized to false so the selected axis will be used in the feature.

## Syntax

"revolveFeatureInput_var" is a variable referencing a RevolveFeatureInput object.  

```python
# Get the value of the property.
propertyValue = revolveFeatureInput_var.isProjectAxis

# Set the value of the property.
revolveFeatureInput_var.isProjectAxis = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2023  

