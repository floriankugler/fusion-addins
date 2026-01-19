# ConstructionAxis.errorOrWarningMessage Property

Parent Object: [ConstructionAxis](ConstructionAxis.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"constructionAxis_var" is a variable referencing a ConstructionAxis object.  

```python
# Get the value of the property.
propertyValue = constructionAxis_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Construction Axis API Sample](ConstructionAxisSample_Sample.md) | Demonstrates creating construction axis in various ways. |

## Version

Introduced in version July 2016  

