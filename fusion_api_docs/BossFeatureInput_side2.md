# BossFeatureInput.side2 Property

Parent Object: [BossFeatureInput](BossFeatureInput.md)  

## Description

Gets or sets inputs for bottom side of the boss feature connection. It is the side where screw thread engages with the part or metal insert. Default Side2 direction is considered opposite to the direction Z-axis of the parent sketch for selected position point.

## Syntax

"bossFeatureInput_var" is a variable referencing a BossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = bossFeatureInput_var.side2

# Set the value of the property.
bossFeatureInput_var.side2 = propertyValue
```

## Property Value

This is a read/write property whose value is a [BossFeatureSideInput](BossFeatureSideInput.md).

## Samples

| Name | Description |
|----|----|
| [Boss Feature Sample](BossFeatureSample_Sample.md) | Demonstrates creating a new boss feature |

## Version

Introduced in version October 2022  

