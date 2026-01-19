# SweepFeatures.createInput Method

Parent Object: [SweepFeatures](SweepFeatures.md)  

## Description

Creates a SweepFeatureInput object for defining a simple sweep feature with only a path and no guide rail or surface. Use properties and methods on this object to define the sweep you want to create and then use the Add method, passing in the SweepFeatureInput object.

## Syntax

"sweepFeatures_var" is a variable referencing a [SweepFeatures](SweepFeatures.md) object.

```python
returnValue = sweepFeatures_var.createInput(profile, path, operation)
```

## Return Value

| Type | Description |
|----|----|
| [SweepFeatureInput](SweepFeatureInput.md) | Returns the newly created SweepFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| profile | [Base](Base.md) | The profile argument can be a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. |
| path | [Path](Path.md) | The path to create the sweep. |
| operation | [FeatureOperations](FeatureOperations.md) | The feature operation to perform |

## Samples

| Name | Description |
|----|----|
| [sweepFeatures.add](sweepFeatures_add_Sample.md) | Demonstrates the sweepFeatures.add method. |
| [Sweep Feature API Sample](SweepFeatureSample_Sample.md) | Demonstrates creating a new sweep feature. |
| [Sweep with guide rail Feature API Sample](SweepWithGuideRailFeatureSample_Sample.md) | Demonstrates creating a new Sweep feature that uses a guide rail along with a profile. |
| [Two Rail Sweep Feature API Sample](TwoRailSweepFeatureSample_Sample.md) | Demonstrates creating new two rail sweep feature. |

## Version

Introduced in version November 2014  

