# ConstantRadiusFilletEdgeSetInput.radius Property

Parent Object: [ConstantRadiusFilletEdgeSetInput](ConstantRadiusFilletEdgeSetInput.md)  

## Description

Gets and sets ValueInput object that defines the radius of the fillet. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length.

## Syntax

"constantRadiusFilletEdgeSetInput_var" is a variable referencing a ConstantRadiusFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = constantRadiusFilletEdgeSetInput_var.radius

# Set the value of the property.
constantRadiusFilletEdgeSetInput_var.radius = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2022  

