# Features.holeFeatures Property

Parent Object: [Features](Features.md)  

## Description

Returns the collection that provides access to the hole features within the component and supports the creation of new hole features.

## Syntax

"features_var" is a variable referencing a Features object.  

```python
# Get the value of the property.
propertyValue = features_var.holeFeatures
```

## Property Value

This is a read only property whose value is a [HoleFeatures](HoleFeatures.md).

## Samples

| Name | Description |
|----|----|
| [holeFeatures.add](holeFeatures_add_Sample.md) | Demonstrates the holeFeatures.add method using the createSimpleInput method. To use this sample, have a design open with a box. Select the face for the hole and two edges to define the position of the hole. |
| [holeFeatures.add with Counterbore](holeFeaturesCounterBore_add_Sample.md) | Demonstrates the holeFeatures.add method using the createCounterboreInput method. The hole is positioned at the center of the selected edge. |
| [holeFeatures.add with Countersink](holeFeaturesCounterSink_add_Sample.md) | Demonstrates the holeFeatures.add method using the createCountersinkInput method and postions the hole in the center of a selected circular edge. |

## Version

Introduced in version August 2014  

