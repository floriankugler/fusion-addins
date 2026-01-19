# BossFeatureInput.side1 Property

Parent Object: [BossFeatureInput](BossFeatureInput.md)  

## Description

Gets or sets inputs for top side of the boss feature connection. It is the side where screw head engages with the boss. Default Side1 direction is considered direction of Z-axis of the parent sketch for selected position point.

## Syntax

"bossFeatureInput_var" is a variable referencing a BossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = bossFeatureInput_var.side1

# Set the value of the property.
bossFeatureInput_var.side1 = propertyValue
```

## Property Value

This is a read/write property whose value is a [BossFeatureSideInput](BossFeatureSideInput.md).

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

