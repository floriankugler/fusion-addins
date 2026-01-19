# BossFeatureSideInput.setCountersink Method

Parent Object: [BossFeatureSideInput](BossFeatureSideInput.md)  

## Description

Set boss shape into constant diameter shank with countersink hole.

## Syntax

"bossFeatureSideInput_var" is a variable referencing a [BossFeatureSideInput](BossFeatureSideInput.md) object.

```python
# Uses no optional arguments.
returnValue = bossFeatureSideInput_var.setCountersink(diameter, holeDiameter, holeMajorDiameter, depth)

# Uses optional arguments.
returnValue = bossFeatureSideInput_var.setCountersink(diameter, holeDiameter, holeMajorDiameter, depth, countersinkAngle)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| diameter | [ValueInput](ValueInput.md) | The outside diameter for the boss feature shank. |
| holeDiameter | [ValueInput](ValueInput.md) | The hole diameter. |
| holeMajorDiameter | [ValueInput](ValueInput.md) | The hole major (or countersink) diameter. |
| depth | [ValueInput](ValueInput.md) | With respect to hole orientation in the boss feature the parameter is either the counterbore depth or thickness of the material under the screw head. |
| countersinkAngle | [ValueInput](ValueInput.md) | Optional parameter for hole countersink angle. If not specified it is set to 90 deg. This is an optional argument whose default value is null. |

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

