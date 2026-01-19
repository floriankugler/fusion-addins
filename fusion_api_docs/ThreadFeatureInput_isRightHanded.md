# ThreadFeatureInput.isRightHanded Property

Parent Object: [ThreadFeatureInput](ThreadFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets if the thread is right or left-handed thread. A value of true indicates a right-handed thread. It defaults to true.

## Remarks

The direction of the thread is now controlled through the isRightHanded property of the ThreadInfo object.

## Syntax

"threadFeatureInput_var" is a variable referencing a ThreadFeatureInput object.  

```python
# Get the value of the property.
propertyValue = threadFeatureInput_var.isRightHanded

# Set the value of the property.
threadFeatureInput_var.isRightHanded = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  
Retired in version September 2025  

