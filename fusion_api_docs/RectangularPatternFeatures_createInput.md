# RectangularPatternFeatures.createInput Method

Parent Object: [RectangularPatternFeatures](RectangularPatternFeatures.md)  

## Description

Creates a RectangularPatternFeatureInput object. Use properties and methods on this object to define the rectangular pattern you want to create and then use the Add method, passing in the RectangularPatternFeatureInput object.

## Syntax

"rectangularPatternFeatures_var" is a variable referencing a [RectangularPatternFeatures](RectangularPatternFeatures.md) object.

```python
returnValue = rectangularPatternFeatures_var.createInput(inputEntities, directionOneEntity, quantityOne, distanceOne, patternDistanceType)
```

## Return Value

| Type | Description |
|----|----|
| [RectangularPatternFeatureInput](RectangularPatternFeatureInput.md) | Returns the newly created RectangularPatternFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | [ObjectCollection](ObjectCollection.md) | The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences. |
| directionOneEntity | [Base](Base.md) | Specifies the entity used to define the first direction entity. This can be a linear edge, construction axis, sketch line or rectangular pattern feature. If a rectangular pattern feature is set, the directionOneEntity and directionTwoEntity properties return the same rectangular pattern feature. |
| quantityOne | [ValueInput](ValueInput.md) | Specifies the number of instances in the first direction. |
| distanceOne | [ValueInput](ValueInput.md) | Specifies the distance in the first direction. How this value is used depends on the value of the PatternDistanceType property. A negative value can be used to change the direction. If the value is ExtentPatternDistanceType then it defines the total distance of the pattern. If the value is SpacingPatternDistanceType then it defines the distance between each element. |
| patternDistanceType | [PatternDistanceType](PatternDistanceType.md) | Specifies how the distance between elements is computed. |

## Samples

| Name | Description |
|----|----|
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |
| [rectangularPattern.add](rectangularPatter_add_Sample.md) | Demonstrates the rectangularPattern.add method using a selected body and two selected edges to define the directions. |

## Version

Introduced in version November 2014  

