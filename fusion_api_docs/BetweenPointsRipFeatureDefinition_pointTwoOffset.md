# BetweenPointsRipFeatureDefinition.pointTwoOffset Property

Parent Object: [BetweenPointsRipFeatureDefinition](BetweenPointsRipFeatureDefinition.md)  

## Description

Gets the ModelParameter that defines the offset for the second point of a between points rip. This is the physical distance from the topological start of the edge. If the offset is either negative, or exceeds the edge length, then the point will be taken as the corresponding vertex of the edge. Returns null if the first point is defined by a vertex. The value can be edited by using the properties of the returned ModelParameter object.

## Syntax

"betweenPointsRipFeatureDefinition_var" is a variable referencing a BetweenPointsRipFeatureDefinition object.  

```python
# Get the value of the property.
propertyValue = betweenPointsRipFeatureDefinition_var.pointTwoOffset
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version September 2023  

