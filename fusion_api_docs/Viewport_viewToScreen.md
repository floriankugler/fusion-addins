# Viewport.viewToScreen Method

Parent Object: [Viewport](Viewport.md)  

## Description

Converts a 2D viewPort point into the equivalent screen coordinate.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.viewToScreen(viewCoordinate)
```

## Return Value

| Type | Description |
|----|----|
| [Point2D](Point2D.md) | Returns the equivalent point in the screen. This can return null in the case where the input point is outside the bounds of the screen, which also means it's outside any viewport. |

## Parameters

| Name | Type | Description |
|----|----|----|
| viewCoordinate | [Point2D](Point2D.md) | A 2D coordinate in the viewport. (0,0) indicates the upper-left corner of the viewport. |

## Version

Introduced in version April 2017  

