# FlatPatternProduct.allParameters Property

Parent Object: [FlatPatternProduct](FlatPatternProduct.md)  

## Description

Returns a read only list of all parameters in the design. This includes the user parameters and model parameters from all components in this design. The parameters from Externally Referenced components are NOT included because they are in actuality, separate designs.

## Syntax

"flatPatternProduct_var" is a variable referencing a FlatPatternProduct object.  

```python
# Get the value of the property.
propertyValue = flatPatternProduct_var.allParameters
```

## Property Value

This is a read only property whose value is a [ParameterList](ParameterList.md).

## Version

Introduced in version October 2022  

