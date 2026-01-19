# SweepFeatureInput.orientation Property

Parent Object: [SweepFeatureInput](SweepFeatureInput.md)  

## Description

Gets and sets the sweep orientation. It defaults to PerpendicularOrientationType. This property is ignored when sweeping a solid or a guide rail or surface has been specified.

## Syntax

"sweepFeatureInput_var" is a variable referencing a SweepFeatureInput object.  

```python
# Get the value of the property.
propertyValue = sweepFeatureInput_var.orientation

# Set the value of the property.
sweepFeatureInput_var.orientation = propertyValue
```

## Property Value

This is a read/write property whose value is a [SweepOrientationTypes](SweepOrientationTypes.md).

## Samples

| Name | Description |
|----|----|
| [sweepFeatures.add](sweepFeatures_add_Sample.md) | Demonstrates the sweepFeatures.add method. |

## Version

Introduced in version November 2014  

