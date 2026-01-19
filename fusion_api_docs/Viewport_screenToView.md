# Viewport.screenToView Method

Parent Object: [Viewport](Viewport.md)  

## Description

Converts a 2D screen point into the equivalent viewport coordinate.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.screenToView(screenCoordinate)
```

## Return Value

| Type | Description |
|----|----|
| [Point2D](Point2D.md) | Returns the equivalent point in the viewport. This can return null in the case where the input screen point does not lie within the viewport. |

## Parameters

| Name | Type | Description |
|----|----|----|
| screenCoordinate | [Point2D](Point2D.md) | A 2D coordinate in screen space. (0,0) indicates the upper-left corner of the entire screen. |

## Version

Introduced in version April 2017  

