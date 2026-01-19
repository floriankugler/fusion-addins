# ArrangeSelection.customRotationX Property

Parent Object: [ArrangeSelection](ArrangeSelection.md)  

## Description

Gets and sets the rotation increments (in degrees) for the x-axis. This function is not available in Fusion for Personal Use. Throws an exception when calling this function in Fusion for Personal Use. To enable any rotation the parameter "arrange_rotation_group" of the operation must be set to true. To disable x-axis rotation for this selection, customRotationX must be set to 0. The default value for this property is 45 degrees. Note: If customRotationX is called, isUsingCustomRotationX will be set to true automatically.

## Syntax

"arrangeSelection_var" is a variable referencing an ArrangeSelection object.  

```python
# Get the value of the property.
propertyValue = arrangeSelection_var.customRotationX

# Set the value of the property.
arrangeSelection_var.customRotationX = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2025  

