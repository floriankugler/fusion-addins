# DecalInput.targetBaseFeature Property

Parent Object: [DecalInput](DecalInput.md)  

## Description

When creating a feature that is owned by a base feature, set this property to the base feature you want to associate the new feature with. By default, this is null, meaning it will not be associated with a base feature.  

Because of a current limitation, if you want to create a feature associated with a base feature, you must set this property AND call the startEdit method of the base feature, create the feature, and then call the finishEdit method of the base feature. The base feature must be in an "edit" state to be able to add any additional items to it.

## Syntax

"decalInput_var" is a variable referencing a DecalInput object.  

```python
# Get the value of the property.
propertyValue = decalInput_var.targetBaseFeature

# Set the value of the property.
decalInput_var.targetBaseFeature = propertyValue
```

## Property Value

This is a read/write property whose value is a [BaseFeature](BaseFeature.md).

## Version

Introduced in version September 2024  

