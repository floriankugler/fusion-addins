# BossFeatureInput.setPositionBySketchPoints Method

Parent Object: [BossFeatureInput](BossFeatureInput.md)  

## Description

Defines the position and orientation of the boss feature using a sketch point(s).

## Syntax

"bossFeatureInput_var" is a variable referencing a [BossFeatureInput](BossFeatureInput.md) object.

```python
returnValue = bossFeatureInput_var.setPositionBySketchPoints(pointOrPoints)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| pointOrPoints | [Base](Base.md) | The sketch point or ObjectCollection of sketch points that defines the position(s) for boss mating location. The orientation of the boss feature is inferred from the normal (Z-axis) of the point's parent sketch. The natural direction (or direction of the screw) will be opposite the normal of the sketch. If multiple sketch points are provided all must belong to the same sketch. Participant bodies will be inferred from closest visible bodies unless specified explicitly. |

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

