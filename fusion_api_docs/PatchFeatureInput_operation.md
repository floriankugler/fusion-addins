# PatchFeatureInput.operation Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

Gets and sets the type of operation performed by the patch feature. Only 'NewBodyFeatureOperation' and 'NewComponentFeatureOperation' are valid operations for patch features.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.operation

# Set the value of the property.
patchFeatureInput_var.operation = propertyValue
```

## Property Value

This is a read/write property whose value is a [FeatureOperations](FeatureOperations.md).

## Version

Introduced in version July 2016  

