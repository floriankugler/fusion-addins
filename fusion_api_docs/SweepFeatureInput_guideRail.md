# SweepFeatureInput.guideRail Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the guide rail to create the sweep. This can be set to null to remove the guide rail definition and have a single path sweep feature.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.guideRail

# Set the value of the property.
sweepFeatureInput_var.guideRail = propertyValue
```

## Property Value

This is a read/write property whose value is a [Path](Path.md).

## Samples

| Name | Description |
|----|----|
| [Sweep with guide rail Feature API Sample](SweepWithGuideRailFeatureSample_Sample.md) | Demonstrates creating a new Sweep feature that uses a guide rail along with a profile. |
| [Two Rail Sweep Feature API Sample](TwoRailSweepFeatureSample_Sample.md) | Demonstrates creating new two rail sweep feature. |

## Version

Introduced in version November 2015  

