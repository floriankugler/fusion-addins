# HoleFeatureInput.setDistanceExtent Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Defines the depth of the hole using a specified distance.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setDistanceExtent(distance)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true if setting the extent was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| distance | [ValueInput](ValueInput.md) | The depth of the hole. If a real is specified the value is in centimeters. If a string is specified the units are derived from the string. If no units are specified, the default units of the document are used. |

## Samples

| Name | Description |
|----|----|
| [holeFeatures.add](holeFeatures_add_Sample.md) | Demonstrates the holeFeatures.add method using the createSimpleInput method. To use this sample, have a design open with a box. Select the face for the hole and two edges to define the position of the hole. |
| [Hole Feature API Sample](HoleFeatureSample_Sample.md) | Demonstrates creating a new hole feature. |
| [holeFeatures.add with Counterbore](holeFeaturesCounterBore_add_Sample.md) | Demonstrates the holeFeatures.add method using the createCounterboreInput method. The hole is positioned at the center of the selected edge. |
| [holeFeatures.add with Countersink](holeFeaturesCounterSink_add_Sample.md) | Demonstrates the holeFeatures.add method using the createCountersinkInput method and postions the hole in the center of a selected circular edge. |

## Version

Introduced in version August 2014  

