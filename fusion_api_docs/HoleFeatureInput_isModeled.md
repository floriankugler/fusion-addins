# HoleFeatureInput.isModeled Property

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Gets and sets if the thread is physical or cosmetic thread. A value of true indicates a physical thread. It defaults to false.  

This property is only used when creating a tapped hole, which means the setToTappedHole method has been called. Otherwise this property is ignored.

## Syntax

"holeFeatureInput_var" is a variable referencing a HoleFeatureInput object.  

```python
# Get the value of the property.
propertyValue = holeFeatureInput_var.isModeled

# Set the value of the property.
holeFeatureInput_var.isModeled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2025  

