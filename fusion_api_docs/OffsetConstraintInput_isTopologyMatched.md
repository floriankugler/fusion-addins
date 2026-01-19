# OffsetConstraintInput.isTopologyMatched Property

Parent Object: [OffsetConstraintInput](OffsetConstraintInput.md)  

## Description

Specifies if the offset curves must match the topology of the original curves. For example, if you have a sketch containing two lines with a fillet (arc) connecting them and offset them inward more than the arc radius, the resulting offset will be two lines. This is a change in topology because the original curves were line-arc-line, and the offset is line-line. An offset of less than the radius still results in a line-arc-line result. If this property is true, indicating the topology must match, creating the offset with a value greater than the arc radius will fail because the result will not have a matching topology.  

When the OffsetConstraintInput is created, this property default to true.

## Syntax

"offsetConstraintInput_var" is a variable referencing an OffsetConstraintInput object.  

```python
# Get the value of the property.
propertyValue = offsetConstraintInput_var.isTopologyMatched

# Set the value of the property.
offsetConstraintInput_var.isTopologyMatched = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2024  

