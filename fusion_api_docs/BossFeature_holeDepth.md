# BossFeature.holeDepth Property

Parent Object: [BossFeature](BossFeature.md)  

## Description

Returns the model parameter controlling the hole depth with respect to hole extent type. If hole extent type is set to BossHoleThrough parameter not used. If hole extent type is BossBlindFull the parameter is a distance from farthest face. If hole extent type is set to BossBlindDepth the parameter is a distance from start face of the hole.

## Syntax

"bossFeature_var" is a variable referencing a BossFeature object.  

```python
# Get the value of the property.
propertyValue = bossFeature_var.holeDepth
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version October 2022  

