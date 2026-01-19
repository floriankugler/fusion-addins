# HoleFeatureInput.isFullLength Property

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Gets and sets if this thread is the full length of the hole. It defaults to true.  

This property is only used when creating a tapped hole, which means the setToTappedHole method has been called. Otherwise this property is ignored.  

The property can only be set to True, which will cause the feature to ignore the values of the threadLength and threadOffset properties. Using the setLengthAndOffset method will have the side effect of setting this property to false.

## Syntax

"holeFeatureInput_var" is a variable referencing a HoleFeatureInput object.  

```python
# Get the value of the property.
propertyValue = holeFeatureInput_var.isFullLength

# Set the value of the property.
holeFeatureInput_var.isFullLength = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2025  

