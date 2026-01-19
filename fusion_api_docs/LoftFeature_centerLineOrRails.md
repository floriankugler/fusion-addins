# LoftFeature.centerLineOrRails Property

Parent Object: [LoftFeature](LoftFeature.md)  

## Description

Returns the single centerline or the set of rails that define the shape of the loft.  

This property returns null in the case where the feature is non-parametric.

## Syntax

"loftFeature_var" is a variable referencing a LoftFeature object.  

```python
# Get the value of the property.
propertyValue = loftFeature_var.centerLineOrRails
```

## Property Value

This is a read only property whose value is a [LoftCenterLineOrRails](LoftCenterLineOrRails.md).

## Version

Introduced in version August 2016  

