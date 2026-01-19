# Design.derivedParameters Property

Parent Object: [Design](Design.md)  

## Description

Returns a read only list of all parameters that are derived into the design. This includes the user parameters and model parameters from all derives in this design.

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.derivedParameters
```

## Property Value

This is a read only property whose value is an array of type [DerivedParameter](DerivedParameter.md).

## Version

Introduced in version January 2026  

