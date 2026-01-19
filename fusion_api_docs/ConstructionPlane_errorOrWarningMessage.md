# ConstructionPlane.errorOrWarningMessage Property

Parent Object: [ConstructionPlane](ConstructionPlane.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"constructionPlane_var" is a variable referencing a ConstructionPlane object.  

```python
# Get the value of the property.
propertyValue = constructionPlane_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Construction Plane API Sample](ConstructionPlaneSample_Sample.md) | Demonstrates creating construction plane by different ways. |

## Version

Introduced in version July 2016  

