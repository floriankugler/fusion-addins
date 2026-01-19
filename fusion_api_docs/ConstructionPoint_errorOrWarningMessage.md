# ConstructionPoint.errorOrWarningMessage Property

Parent Object: [ConstructionPoint](ConstructionPoint.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"constructionPoint_var" is a variable referencing a ConstructionPoint object.  

```python
# Get the value of the property.
propertyValue = constructionPoint_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Construction Point API Sample](ConstructionPointSample_Sample.md) | Demonstrates creating construction point by different ways |

## Version

Introduced in version July 2016  

