# Features.chamferFeatures Property

Parent Object: [Features](Features.md)  

## Description

Returns the collection that provides access to the chamfer features within the component and supports the creation of new chamfer features.

## Syntax

"features_var" is a variable referencing a Features object.  

```python
# Get the value of the property.
propertyValue = features_var.chamferFeatures
```

## Property Value

This is a read only property whose value is a [ChamferFeatures](ChamferFeatures.md).

## Samples

| Name | Description |
|----|----|
| [chamferFeatures.add](chamferFeatures_add_Sample.md) | Demonstrates the chamferFeatures.add method. To use this sample have a part open that contains a body. When you run the script, you will be prompted to select an edge to chamfer. |
| [Equal Distance Chamfer Feature API Sample](EqualDistanceChamferFeature_Sample.md) | Creates an equal distance chamfer on the selected edge. If there are tangent contiguous edges that will also be included in the chamfer. |

## Version

Introduced in version November 2014  

