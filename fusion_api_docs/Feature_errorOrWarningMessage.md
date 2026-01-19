# Feature.errorOrWarningMessage Property

Parent Object: [Feature](Feature.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"feature_var" is a variable referencing a Feature object.  

```python
# Get the value of the property.
propertyValue = feature_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version July 2016  

