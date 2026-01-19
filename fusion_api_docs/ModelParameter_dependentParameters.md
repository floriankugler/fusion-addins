# ModelParameter.dependentParameters Property

Parent Object: [ModelParameter](ModelParameter.md)  

## Description

Returns a list of parameters that are dependent on this parameter as a result of this parameter being referenced in their equation.

## Syntax

"modelParameter_var" is a variable referencing a ModelParameter object.  

```python
# Get the value of the property.
propertyValue = modelParameter_var.dependentParameters
```

## Property Value

This is a read only property whose value is a [ParameterList](ParameterList.md).

## Version

Introduced in version August 2014  

