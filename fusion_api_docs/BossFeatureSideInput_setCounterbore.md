# BossFeatureSideInput.setCounterbore Method

Parent Object: [BossFeatureSideInput](BossFeatureSideInput.md)  

## Description

Set boss shape into constant diameter shank with counterbore hole.

## Syntax

"bossFeatureSideInput_var" is a variable referencing a [BossFeatureSideInput](BossFeatureSideInput.md) object.

```python
returnValue = bossFeatureSideInput_var.setCounterbore(diameter, holeDiameter, holeMajorDiameter, depth)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| diameter | [ValueInput](ValueInput.md) | The outside diameter for the boss feature shank. |
| holeDiameter | [ValueInput](ValueInput.md) | The hole diameter. |
| holeMajorDiameter | [ValueInput](ValueInput.md) | The hole major (or counterbore) diameter. |
| depth | [ValueInput](ValueInput.md) | With respect to hole orientation in the boss feature the parameter is either the counterbore depth or thickness of the material under the screw head. |

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

