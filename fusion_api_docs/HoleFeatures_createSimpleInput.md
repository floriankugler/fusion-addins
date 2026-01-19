# HoleFeatures.createSimpleInput Method

Parent Object: [HoleFeatures](HoleFeatures.md)  

## Description

Creates a HoleFeatureInput object that defines a simple hole (a single diameter). This is not a hole feature, but an object used to create a hole feature. Functionality on the returned HoleFeatureInput object is used to define the position and extent of the hole.

## Syntax

"holeFeatures_var" is a variable referencing a [HoleFeatures](HoleFeatures.md) object.

```python
returnValue = holeFeatures_var.createSimpleInput(holeDiameter)
```

## Return Value

| Type | Description |
|----|----|
| [HoleFeatureInput](HoleFeatureInput.md) | Returns the newly created HoleFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| holeDiameter | [ValueInput](ValueInput.md) | A ValueInput object that defines the diameter of the hole. If the ValueInput uses a real, it is interpreted as centimeters. If it is a string, the units can be defined as part of the string (i.e. "3 in") If no units are specified, it is interpreted using the current default units for length. If tap information is added to the hole using the returned HoleFeatureInput, it will override this diameter, and the hole will be the correct size for the specified tap. |

## Samples

| Name | Description |
|----|----|
| [holeFeatures.add](holeFeatures_add_Sample.md) | Demonstrates the holeFeatures.add method using the createSimpleInput method. To use this sample, have a design open with a box. Select the face for the hole and two edges to define the position of the hole. |
| [Hole Feature API Sample](HoleFeatureSample_Sample.md) | Demonstrates creating a new hole feature. |

## Version

Introduced in version August 2014  

