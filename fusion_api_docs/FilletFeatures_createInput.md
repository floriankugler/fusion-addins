# FilletFeatures.createInput Method

Parent Object: [FilletFeatures](FilletFeatures.md)  

## Description

Creates a FilletFeatureInput object. Use properties and methods on this object to define the fillet you want to create and then use the Add method, passing in the FilletFeatureInput object.

## Syntax

"filletFeatures_var" is a variable referencing a [FilletFeatures](FilletFeatures.md) object.

```python
returnValue = filletFeatures_var.createInput()
```

## Return Value

| Type | Description |
|----|----|
| [FilletFeatureInput](FilletFeatureInput.md) | Returns the newly created FilletFeatureInput object or null if the creation failed. |

## Samples

| Name | Description |
|----|----|
| [Constant Radius Fillet API Sample](ConstantRadiusFillet_Sample.md) | Creates a constant radius fillet on the selected edge. If there are tangent contiguous edges that will also be included in the fillet. |
| [filletFeatures.add](filletFeatures_add_Sample.md) | Demonstrates the filletFeatures.add method. |
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2014  

