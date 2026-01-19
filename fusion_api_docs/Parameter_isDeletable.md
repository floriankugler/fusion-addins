# Parameter.isDeletable Property

Parent Object: [Parameter](Parameter.md)  

## Description

Gets if this parameter can be deleted. Parameters that have dependents cannot be deleted, and model parameters typically cannot be deleted. However, there is the possibility in uncommon workflows where a model parameter no longer has any dependents, and it was not automatically deleted. In this case, this property will return true, and the deleteMe method can delete the parameter.

## Syntax

"parameter_var" is a variable referencing a Parameter object.  

```python
# Get the value of the property.
propertyValue = parameter_var.isDeletable
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version September 2015  

