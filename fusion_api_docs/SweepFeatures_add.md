# SweepFeatures.add Method

Parent Object: [SweepFeatures](SweepFeatures.md)  

## Description

Creates a new sweep feature.

## Syntax

"sweepFeatures_var" is a variable referencing a [SweepFeatures](SweepFeatures.md) object.

```python
returnValue = sweepFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [SweepFeature](SweepFeature.md) | Returns the newly created SweepFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [SweepFeatureInput](SweepFeatureInput.md) | A SweepFeatureInput object that defines the desired sweep. Use the createInput method to create a new SweepFeatureInput object and then use methods on it (the SweepFeatureInput object) to define the sweep. |

## Samples

| Name | Description |
|----|----|
| [sweepFeatures.add](sweepFeatures_add_Sample.md) | Demonstrates the sweepFeatures.add method. |
| [Sweep Feature API Sample](SweepFeatureSample_Sample.md) | Demonstrates creating a new sweep feature. |
| [Sweep with guide rail Feature API Sample](SweepWithGuideRailFeatureSample_Sample.md) | Demonstrates creating a new Sweep feature that uses a guide rail along with a profile. |
| [Two Rail Sweep Feature API Sample](TwoRailSweepFeatureSample_Sample.md) | Demonstrates creating new two rail sweep feature. |

## Version

Introduced in version November 2014  

