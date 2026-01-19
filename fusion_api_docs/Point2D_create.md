# Point2D.create Method

Parent Object: [Point2D](Point2D.md)  

## Description

Creates a transient 2D point object.

## Syntax

This is a static method.  

```python

# Uses no optional arguments.
returnValue = adsk.core.Point2D.create()

# Uses optional arguments.
returnValue = adsk.core.Point2D.create(x, y)
```

## Return Value

| Type | Description |
|----|----|
| [Point2D](Point2D.md) | Returns the new Point2D object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| x | double | The x coordinate of the point This is an optional argument whose default value is 0.0. |
| y | double | The y coordinate of the point This is an optional argument whose default value is 0.0. |

## Version

Introduced in version August 2014  

