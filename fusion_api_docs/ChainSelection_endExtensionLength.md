# ChainSelection.endExtensionLength Property

Parent Object: [ChainSelection](ChainSelection.md)  

## Description

Property that gets and sets the length of the extension of an open curve at the end of the chain. The value is specified in centimeters. This is only applicable to open contours and when DistanceCap is chosen as the extension cap.

## Syntax

"chainSelection_var" is a variable referencing a ChainSelection object.  

```python
# Get the value of the property.
propertyValue = chainSelection_var.endExtensionLength

# Set the value of the property.
chainSelection_var.endExtensionLength = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version April 2023  

