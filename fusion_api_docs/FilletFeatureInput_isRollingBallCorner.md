# FilletFeatureInput.isRollingBallCorner Property

Parent Object: [FilletFeatureInput](FilletFeatureInput.md)  

## Description

Gets and sets if a rolling ball or setback solution is to be used in any corners. For an asymmetric fillet only a setback solution is supported, so any asymmetric edge sets will ignore this setting and will always be a setback corner.

## Syntax

"filletFeatureInput_var" is a variable referencing a FilletFeatureInput object.  

```python
# Get the value of the property.
propertyValue = filletFeatureInput_var.isRollingBallCorner

# Set the value of the property.
filletFeatureInput_var.isRollingBallCorner = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2014  

