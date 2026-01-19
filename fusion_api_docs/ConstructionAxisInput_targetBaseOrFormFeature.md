# ConstructionAxisInput.targetBaseOrFormFeature Property

Parent Object: [ConstructionAxisInput](ConstructionAxisInput.md)  

## Description

When creating a construction axis that is owned by a base or form feature, set this property to the base or form feature you want to associate the new construction plane with. By default, this is null, meaning it will not be associated with a base or form feature.  

Because of a current limitation, if you want to create a construction axis associated with a base or form feature, you must set this property AND call the startEdit method of the base or form feature, create the feature, and then call the finishEdit method of the base or form feature. The base or form feature must be in an "edit" state to be able to add any additional items to it.

## Syntax

"constructionAxisInput_var" is a variable referencing a ConstructionAxisInput object.  

```python
# Get the value of the property.
propertyValue = constructionAxisInput_var.targetBaseOrFormFeature

# Set the value of the property.
constructionAxisInput_var.targetBaseOrFormFeature = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version May 2016  

