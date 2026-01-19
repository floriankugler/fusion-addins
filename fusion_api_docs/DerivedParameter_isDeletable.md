# DerivedParameter.isDeletable Property

Parent Object: [DerivedParameter](DerivedParameter.md)  

## Description

Gets if this parameter can be deleted. Parameters that have dependents cannot be deleted, and model parameters typically cannot be deleted. However, there is the possibility in uncommon workflows where a model parameter no longer has any dependents, and it was not automatically deleted. In this case, this property will return true, and the deleteMe method can delete the parameter.

## Syntax

"derivedParameter_var" is a variable referencing a DerivedParameter object.  

```python
# Get the value of the property.
propertyValue = derivedParameter_var.isDeletable
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2026  

