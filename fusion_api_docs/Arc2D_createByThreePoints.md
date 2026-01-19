# Arc2D.createByThreePoints Method

Parent Object: [Arc2D](Arc2D.md)  

## Description

Creates a transient 2D arc by specifying 3 points. A transient arc is not displayed or saved in a document. Transient arcs are used as a wrapper to work with raw 2D arc information.

## Syntax

This is a static method.  

```python

returnValue = adsk.core.Arc2D.createByThreePoints(startPoint, point, endPoint)
```

## Return Value

| Type | Description |
|----|----|
| [Arc2D](Arc2D.md) | Returns the newly created arc or null if the creation failed. |

## Parameters

| Name       | Type                   | Description                 |
|------------|------------------------|-----------------------------|
| startPoint | [Point2D](Point2D.md) | The start point of the arc. |
| point      | [Point2D](Point2D.md) | A point along the arc.      |
| endPoint   | [Point2D](Point2D.md) | The end point of the arc.   |

## Version

Introduced in version August 2014  

