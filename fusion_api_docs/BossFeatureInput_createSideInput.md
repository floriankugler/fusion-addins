# BossFeatureInput.createSideInput Method

Parent Object: [BossFeatureInput](BossFeatureInput.md)  

## Description

Creates a new BossFeatureSideInput object that is used to specify the input for boss feature side. This object can be set to side1 or side2. Side1 is meant to be side where screw head engages with the boss and Side2 is meant to be a side where screw thread engages with the part or metal inserts.

## Syntax

"bossFeatureInput_var" is a variable referencing a [BossFeatureInput](BossFeatureInput.md) object.

```python
returnValue = bossFeatureInput_var.createSideInput()
```

## Return Value

| Type | Description |
|----|----|
| [BossFeatureSideInput](BossFeatureSideInput.md) | Returns BossFeatureSideInput if successful. |

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

