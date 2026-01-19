# RectangularPatternFeatureInput.setDirectionTwo Method

Parent Object: [RectangularPatternFeatureInput](RectangularPatternFeatureInput.md)  

## Description

Sets all of the input required to define the pattern in the second direction.

## Syntax

"rectangularPatternFeatureInput_var" is a variable referencing a [RectangularPatternFeatureInput](RectangularPatternFeatureInput.md) object.

```python
returnValue = rectangularPatternFeatureInput_var.setDirectionTwo(directionTwoEntity, quantityTwo, distanceTwo)
```

## Return Value

| Type    | Description                        |
|---------|------------------------------------|
| boolean | Returns true if it was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| directionTwoEntity | [Base](Base.md) | Specifies the entity used to define the second direction entity. This can be a linear edge, construction axis, sketch line or rectangular pattern feature. If a rectangular pattern feature is set, the directionOneEntity and directionTwoEntity properties return the same rectangular pattern feature. This argument can be null to indicate that the default second direction is to be used, which is 90 degrees to the first direction. |
| quantityTwo | [ValueInput](ValueInput.md) | Specifies the number of instances in the second direction. |
| distanceTwo | [ValueInput](ValueInput.md) | Specifies the distance in the second direction. How this value is used depends on the value of the PatternDistanceType property. If the value is ExtentPatternDistanceType then it defines the total distance of the pattern. If the value is SpacingPatternDistanceType then it defines the distance between each element. |

## Samples

| Name | Description |
|----|----|
| [Manage Participant Bodies API Sample](ParticipantBodiesSample_Sample.md) | Demonstrates how to manage participant During Cut operation. Same API can be used to manage participants During intersection also. |

## Version

Introduced in version November 2014  

