# RectangularPatternConstraintInput.setDirectionTwo Method

Parent Object: [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md)  

## Description

Sets all of the input required to define the pattern in the second direction.

## Syntax

"rectangularPatternConstraintInput_var" is a variable referencing a [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md) object.

```python
returnValue = rectangularPatternConstraintInput_var.setDirectionTwo(directionTwoEntity, quantityTwo, distanceTwo)
```

## Return Value

| Type    | Description                        |
|---------|------------------------------------|
| boolean | Returns true if it was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| directionTwoEntity | [SketchLine](SketchLine.md) | Specifies the SketchLine object used to define the second direction entity. This argument can be null to indicate that the default second direction is to be used, which is 90 degrees to the first direction. |
| quantityTwo | [ValueInput](ValueInput.md) | Specifies the number of instances in the second direction. |
| distanceTwo | [ValueInput](ValueInput.md) | Specifies the distance in the second direction. How this value is used depends on the value of the PatternDistanceType property. If the value is ExtentPatternDistanceType then it defines the total distance of the pattern. If the value is SpacingPatternDistanceType then it defines the distance between each element. |

## Version

Introduced in version September 2022  

