# FilletFeature.deleteMe Method

Parent Object: [FilletFeature](FilletFeature.md)  

## Description

Deletes the feature. This works for both parametric and non-parametric features.

## Syntax

"filletFeature_var" is a variable referencing a [FilletFeature](FilletFeature.md) object.

```python
returnValue = filletFeature_var.deleteMe()
```

## Return Value

| Type    | Description                                                    |
|---------|----------------------------------------------------------------|
| boolean | Returns a bool indicating if the delete was successful or not. |

## Samples

| Name | Description |
|----|----|
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2014  

