# FormFeature.linkedFeatures Property

Parent Object: [FormFeature](FormFeature.md)  

## Description

Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface.

## Syntax

"formFeature_var" is a variable referencing a FormFeature object.  

```python
# Get the value of the property.
propertyValue = formFeature_var.linkedFeatures
```

## Property Value

This is a read only property whose value is a [FeatureList](FeatureList.md).

## Version

Introduced in version September 2015  

