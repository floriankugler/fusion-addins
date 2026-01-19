# WorkingModel.allParameters Property

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Returns a read only list of all parameters in the design. This includes the user parameters and model parameters from all components in this design. The parameters from Externally Referenced components are NOT included because they are in actuality, separate designs.

## Syntax

"workingModel_var" is a variable referencing a WorkingModel object.  

```python
# Get the value of the property.
propertyValue = workingModel_var.allParameters
```

## Property Value

This is a read only property whose value is a [ParameterList](ParameterList.md).

## Version

Introduced in version January 2024  

