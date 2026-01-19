# ChainSelection.isOpen Property

Parent Object: [ChainSelection](ChainSelection.md)  

## Description

Property to get or set if an open contour should be closed or not. If true and the input does not specify a closed contour, additional curve segments will be generated to close the contour.

## Syntax

"chainSelection_var" is a variable referencing a ChainSelection object.  

```python
# Get the value of the property.
propertyValue = chainSelection_var.isOpen

# Set the value of the property.
chainSelection_var.isOpen = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version April 2023  

