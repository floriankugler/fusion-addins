# ArrangeSelection.isUsingCustomRotationX Property

Parent Object: [ArrangeSelection](ArrangeSelection.md)  

## Description

Gets and sets if custom rotation is used for the x-axis. This function is not available in Fusion for Personal Use. Throws an exception when calling this function in Fusion for Personal Use. To enable any rotation the parameter "arrange_rotation_group" of the operation must be set to true. If isUsingCustomRotationX is false, the rotation of the operation's parameter "arrange_rotation_x" is used. The default value for this property false.

## Syntax

"arrangeSelection_var" is a variable referencing an ArrangeSelection object.  

```python
# Get the value of the property.
propertyValue = arrangeSelection_var.isUsingCustomRotationX

# Set the value of the property.
arrangeSelection_var.isUsingCustomRotationX = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

