# Arc2D.set Method

Parent Object: [Arc2D](Arc2D.md)  

## Description

Sets all of the data defining the arc.

## Syntax

"arc2D_var" is a variable referencing an [Arc2D](Arc2D.md) object.

```python
returnValue = arc2D_var.set(center, radius, startAngle, endAngle, isClockwise)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if redefining the arc is successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| center | [Point2D](Point2D.md) | A Point2D object defining the center position of the arc. |
| radius | double | The radius of the arc. |
| startAngle | double | The start angle of the arc in radians, where 0 is along the x axis. |
| endAngle | double | The end angle of the arc in radians, where 0 is along the x axis. |
| isClockwise | boolean | Indicates if the sweep direction is clockwise or counterclockwise. |

## Version

Introduced in version August 2014  

