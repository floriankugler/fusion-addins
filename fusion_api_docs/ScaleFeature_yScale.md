# ScaleFeature.yScale Property

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Returns the parameter that controls the Y scale factor. This will return null in the case where isUniform is false or the feature is non-parametric. You can use the properties and methods on the ModelParameter object to get and set the value.

## Syntax

"scaleFeature_var" is a variable referencing a ScaleFeature object.  

```python
# Get the value of the property.
propertyValue = scaleFeature_var.yScale
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2015  

