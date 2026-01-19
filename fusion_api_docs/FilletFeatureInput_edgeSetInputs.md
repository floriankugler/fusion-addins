# FilletFeatureInput.edgeSetInputs Property

Parent Object: [FilletFeatureInput](FilletFeatureInput.md)  

## Description

Gets the FilletEdgeSetInputs object that provides support to create the various types of edge sets that will be used to create the fillet.

## Syntax

"filletFeatureInput_var" is a variable referencing a FilletFeatureInput object.  

```python
# Get the value of the property.
propertyValue = filletFeatureInput_var.edgeSetInputs
```

## Property Value

This is a read only property whose value is a [FilletEdgeSetInputs](FilletEdgeSetInputs.md).

## Samples

| Name | Description |
|----|----|
| [filletFeatures.add](filletFeatures_add_Sample.md) | Demonstrates the filletFeatures.add method. |
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2022  

