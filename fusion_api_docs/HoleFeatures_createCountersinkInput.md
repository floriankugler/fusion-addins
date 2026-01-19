# HoleFeatures.createCountersinkInput Method

Parent Object: [HoleFeatures](HoleFeatures.md)  

## Description

Creates a HoleFeatureInput object that defines a countersink hole. This is not a hole feature but an object used to create a hole feature. Functionality on the returned HoleFeatureInput object is used to define the position and extent of the hole.

## Syntax

"holeFeatures_var" is a variable referencing a [HoleFeatures](HoleFeatures.md) object.

```python
returnValue = holeFeatures_var.createCountersinkInput(holeDiameter, countersinkDiameter, countersinkAngle)
```

## Return Value

| Type | Description |
|----|----|
| [HoleFeatureInput](HoleFeatureInput.md) | Returns the newly created HoleFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| holeDiameter | [ValueInput](ValueInput.md) | A ValueInput object that defines the diameter of the hole. If the ValueInput uses a real, it is interpreted as centimeters. If it is a string, the units can be defined as part of the string (i.e. "3 in") If no units are specified, it is interpreted using the current default units for length. If tap information is added to the hole using the returned HoleFeatureInput, it will override this diameter, and the hole will be the correct size for the specified tap. |
| countersinkDiameter | [ValueInput](ValueInput.md) | A ValueInput object that defines the diameter of the countersink. If the ValueInput uses a real, it is interpreted as centimeters. If it is a string, the units can be defined as part of the string (i.e. "3 in") If no units are specified, it is interpreted using the current default units for length. |
| countersinkAngle | [ValueInput](ValueInput.md) | A ValueInput object that defines the angle of the countersink. If the ValueInput uses a real then it is interpreted as radians. If it is a string then the units can be defined as part of the string (i.e. "120 deg"). If no units are specified it is interpreted using the current default units for angles. |

## Samples

| Name | Description |
|----|----|
| [holeFeatures.add with Countersink](holeFeaturesCounterSink_add_Sample.md) | Demonstrates the holeFeatures.add method using the createCountersinkInput method and postions the hole in the center of a selected circular edge. |

## Version

Introduced in version August 2014  

