# Arc2D.getData Method

Parent Object: [Arc2D](Arc2D.md)  

## Description

Gets all of the data defining the arc.

## Syntax

"arc2D_var" is a variable referencing an [Arc2D](Arc2D.md) object.  

```python
(returnValue, center, radius, startAngle, endAngle, isClockwise) = arc2D_var.getData()
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | The output center point of the arc. |
| radius | double | The output radius of the arc. |
| startAngle | double | The output start angle of the arc in radians, where 0 is along the x axis. |
| endAngle | double | The output end angle of the arc in radians, where 0 is along the x axis. |
| isClockwise | boolean | The output value that indicates if the sweep direction is clockwise or counterclockwise. |

## Version

Introduced in version August 2014  

