# SweepFeature.distanceTwo Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets the distance for the second side. Returns nothing if the path is only on one side of the profile or if the sweep definition includes a guide rail or surface. It's always the distance against the normal of the profile if available. This property returns nothing in the case where the feature is non-parametric.

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.distanceTwo
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2015  

