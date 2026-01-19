# LoftFeatureInput.isSolid Property

Parent Object: [LoftFeatureInput](LoftFeatureInput.md)  

## Description

Specifies if the loft should be created as a solid or surface. This is initialized to true so a solid will attempt to be created if it's not changed.

## Syntax

"loftFeatureInput_var" is a variable referencing a LoftFeatureInput object.  

```python
# Get the value of the property.
propertyValue = loftFeatureInput_var.isSolid

# Set the value of the property.
loftFeatureInput_var.isSolid = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [loftFeatures.add](loftFeatures_add_Sample.md) | Demonstrates the loftFeatures.add method. |
| [Loft Feature API Sample](LoftFeatureSample_Sample.md) | Demonstrates creating a new loft feature. |

## Version

Introduced in version August 2016  

