# AsymmetricFilletEdgeSetInput.offsetOne Property

Parent Object: [AsymmetricFilletEdgeSetInput](AsymmetricFilletEdgeSetInput.md)  

## Description

Gets and sets a ValueInput object that defines the first offset of the asymmetric fillet. If the ValueInput uses a real value then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current document units for length.

## Syntax

"asymmetricFilletEdgeSetInput_var" is a variable referencing an AsymmetricFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = asymmetricFilletEdgeSetInput_var.offsetOne

# Set the value of the property.
asymmetricFilletEdgeSetInput_var.offsetOne = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2025  

