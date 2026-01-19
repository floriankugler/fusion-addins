# BoundaryFillFeatures.add Method

Parent Object: [BoundaryFillFeatures](BoundaryFillFeatures.md)  

## Description

Creates a new boundary fill feature.

## Syntax

"boundaryFillFeatures_var" is a variable referencing a [BoundaryFillFeatures](BoundaryFillFeatures.md) object.

```python
returnValue = boundaryFillFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [BoundaryFillFeature](BoundaryFillFeature.md) | Returns the newly created BoundaryFillFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [BoundaryFillFeatureInput](BoundaryFillFeatureInput.md) | A BoundaryFillFeatureInput object that defines the desired boundary fill feature. Use the createInput method to create a new BoundaryFillFeatureInput object and then use methods on it (the BoundaryFillFeatureInput object) to define the boundary fill feature. |

## Samples

| Name | Description |
|----|----|
| [boundaryFillFeatures.add](boundaryFillFeatures_add_Sample.md) | Demonstrates the boundaryFill.add method. To use this sample you need to have two existing overlapping bodies. You'll be prompted to select the bodies when running the script. |
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |

## Version

Introduced in version June 2015  

