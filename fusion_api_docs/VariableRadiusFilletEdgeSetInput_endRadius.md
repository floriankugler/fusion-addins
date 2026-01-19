# VariableRadiusFilletEdgeSetInput.endRadius Property

Parent Object: [VariableRadiusFilletEdgeSetInput](VariableRadiusFilletEdgeSetInput.md)  

## Description

Gets and sets a ValueInput object that defines the ending radius of the fillet. If a single edge is being filleted, the end radius is at the end of the edge. If multiple tangent edges are being filleted the end radius is the open end of the last edge in the collection.  

If the ValueInput uses a real then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length.

## Syntax

"variableRadiusFilletEdgeSetInput_var" is a variable referencing a VariableRadiusFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = variableRadiusFilletEdgeSetInput_var.endRadius

# Set the value of the property.
variableRadiusFilletEdgeSetInput_var.endRadius = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2022  

