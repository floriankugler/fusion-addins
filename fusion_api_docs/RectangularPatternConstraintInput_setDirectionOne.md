# RectangularPatternConstraintInput.setDirectionOne Method

Parent Object: [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md)  

## Description

Sets all of the input required to define the pattern in the first direction.

## Syntax

"rectangularPatternConstraintInput_var" is a variable referencing a [RectangularPatternConstraintInput](RectangularPatternConstraintInput.md) object.

```python
returnValue = rectangularPatternConstraintInput_var.setDirectionOne(directionOneEntity, quantityOne, distanceOne)
```

## Return Value

| Type    | Description                        |
|---------|------------------------------------|
| boolean | Returns true if it was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| directionOneEntity | [SketchLine](SketchLine.md) | Specifies the SketchLine object used to define the first direction entity. This argument can be null to indicate that the default first direction is to be used, which is along the X axis of the sketch. |
| quantityOne | [ValueInput](ValueInput.md) | Specifies the number of instances in the first direction. |
| distanceOne | [ValueInput](ValueInput.md) | Specifies the distance in the first direction. How this value is used depends on the value of the PatternDistanceType property. If the value is ExtentPatternDistanceType then it defines the total distance of the pattern. If the value is SpacingPatternDistanceType then it defines the distance between each element. |

## Version

Introduced in version September 2022  

