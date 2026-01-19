# ArrangeSelection.isUsingCustomQuantity Property

Parent Object: [ArrangeSelection](ArrangeSelection.md)  

## Description

Gets and sets if custom quantity is used for this element. This function is not available in Fusion for Personal Use. Throws an exception when calling this function in Fusion for Personal Use. If isUsingCustomQuantity is false, the global quantity of the operation's parameter "arrange_global_quantity" is used. The default value for this property false.

## Syntax

"arrangeSelection_var" is a variable referencing an ArrangeSelection object.  

```python
# Get the value of the property.
propertyValue = arrangeSelection_var.isUsingCustomQuantity

# Set the value of the property.
arrangeSelection_var.isUsingCustomQuantity = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

