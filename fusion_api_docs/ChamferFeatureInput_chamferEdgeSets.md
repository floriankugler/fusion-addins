# ChamferFeatureInput.chamferEdgeSets Property

Parent Object: [ChamferFeatureInput](ChamferFeatureInput.md)  

## Description

Returns the collection of edge sets for this chamfer feature input.

## Syntax

"chamferFeatureInput_var" is a variable referencing a ChamferFeatureInput object.  

```python
# Get the value of the property.
propertyValue = chamferFeatureInput_var.chamferEdgeSets
```

## Property Value

This is a read only property whose value is a [ChamferEdgeSets](ChamferEdgeSets.md).

## Samples

| Name | Description |
|----|----|
| [chamferFeatures.add](chamferFeatures_add_Sample.md) | Demonstrates the chamferFeatures.add method. To use this sample have a part open that contains a body. When you run the script, you will be prompted to select an edge to chamfer. |
| [Equal Distance Chamfer Feature API Sample](EqualDistanceChamferFeature_Sample.md) | Creates an equal distance chamfer on the selected edge. If there are tangent contiguous edges that will also be included in the chamfer. |

## Version

Introduced in version December 2020  

