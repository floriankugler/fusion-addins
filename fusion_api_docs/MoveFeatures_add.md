# MoveFeatures.add Method

Parent Object: [MoveFeatures](MoveFeatures.md)  

## Description

Creates a new move feature.

## Syntax

"moveFeatures_var" is a variable referencing a [MoveFeatures](MoveFeatures.md) object.

```python
returnValue = moveFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [MoveFeature](MoveFeature.md) | Returns the newly created MoveFeature object or null if the creation failed. Returns nothing in the case where the feature is non-parametric. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MoveFeatureInput](MoveFeatureInput.md) | A MoveFeatureInput object that defines the desired move feature. Use the createInput2 method to create a new MoveFeatureInput object and then use methods on the MoveFeatureInput object to define the move feature. |

## Samples

| Name | Description |
|----|----|
| [moveFeatures.add](moveFeatures_add_Sample.md) | Demonstrates the moveFeatures.add method. |
| [Move Feature API Sample](MoveFeatureSample_Sample.md) | Demonstrates creating a new move feature. |

## Version

Introduced in version March 2015  

