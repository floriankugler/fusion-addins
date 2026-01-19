# LoftFeature.linkedFeatures Property

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Returns the set of features that are linked to this feature. The set of linked features are all of the features that were created in various components as the result of a single feature being created in the user interface.

## Syntax

"loftFeature_var" is a variable referencing a LoftFeature object.  

```python
# Get the value of the property.
propertyValue = loftFeature_var.linkedFeatures
```

## Property Value

This is a read only property whose value is a [FeatureList](FeatureList.md).

## Version

Introduced in version September 2015  

