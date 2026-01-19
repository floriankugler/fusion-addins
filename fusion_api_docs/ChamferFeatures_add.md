# ChamferFeatures.add Method

Parent Object: [ChamferFeatures](ChamferFeatures.md)  

## Description

Creates a new chamfer feature.

## Syntax

"chamferFeatures_var" is a variable referencing a [ChamferFeatures](ChamferFeatures.md) object.

```python
returnValue = chamferFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [ChamferFeature](ChamferFeature.md) | Returns the newly created ChamferFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [ChamferFeatureInput](ChamferFeatureInput.md) | A ChamferFeatureInput object that defines the desired chamfer. Use the createInput method to create a new ChamferFeatureInput object and then use methods on it (the ChamferFeatureInput object) to define the chamfer. |

## Samples

| Name | Description |
|----|----|
| [chamferFeatures.add](chamferFeatures_add_Sample.md) | Demonstrates the chamferFeatures.add method. To use this sample have a part open that contains a body. When you run the script, you will be prompted to select an edge to chamfer. |
| [Equal Distance Chamfer Feature API Sample](EqualDistanceChamferFeature_Sample.md) | Creates an equal distance chamfer on the selected edge. If there are tangent contiguous edges that will also be included in the chamfer. |

## Version

Introduced in version November 2014  

