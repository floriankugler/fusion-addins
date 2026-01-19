# BossFeatureSideInput.holeDepth Property

Parent Object: [BossFeatureSideInput](BossFeatureSideInput.md)  

## Description

Get or set hole depth with respect to hole extent type. If hole extent type is set to BossHoleThrough parameter is ignored. If hole extent type is BossBlindFull the parameter is a distance from farthest face. If hole extent type is set to BossBlindDepth the parameter is a distance from start face of the hole.

## Syntax

"bossFeatureSideInput_var" is a variable referencing a BossFeatureSideInput object.  

```python
# Get the value of the property.
propertyValue = bossFeatureSideInput_var.holeDepth

# Set the value of the property.
bossFeatureSideInput_var.holeDepth = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

