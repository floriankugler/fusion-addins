# RectangularPatternFeatures.add Method

Parent Object: [RectangularPatternFeatures](RectangularPatternFeatures.md)  

## Description

Creates a new rectangular pattern feature.

## Syntax

"rectangularPatternFeatures_var" is a variable referencing a [RectangularPatternFeatures](RectangularPatternFeatures.md) object.

```python
returnValue = rectangularPatternFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [RectangularPatternFeature](RectangularPatternFeature.md) | Returns the newly created RectangularPatternFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [RectangularPatternFeatureInput](RectangularPatternFeatureInput.md) | A RectangularPatternFeatureInput object that defines the desired rectangular pattern. Use the createInput method to create a new RectangularPatternFeatureInput object and then use methods on it (the RectangularPatternFeatureInput object) to define the rectangular pattern. |

## Samples

| Name | Description |
|----|----|
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |
| [rectangularPattern.add](rectangularPatter_add_Sample.md) | Demonstrates the rectangularPattern.add method using a selected body and two selected edges to define the directions. |

## Version

Introduced in version November 2014  

