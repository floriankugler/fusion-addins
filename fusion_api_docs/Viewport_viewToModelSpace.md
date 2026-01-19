# Viewport.viewToModelSpace Method

Parent Object: [Viewport](Viewport.md)  

## Description

A specified point in view space returns the equivalent point in model space. Because view space is 2D and model space is 3D, the depth of the point is returned is somewhat arbitrary along the eye to target point direction.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.viewToModelSpace(viewCoordinate)
```

## Return Value

| Type                   | Description                                  |
|------------------------|----------------------------------------------|
| [Point3D](Point3D.md) | Returns the equivalent point in model space. |

## Parameters

| Name           | Type                   | Description                 |
|----------------|------------------------|-----------------------------|
| viewCoordinate | [Point2D](Point2D.md) | A coordinate in view space. |

## Version

Introduced in version December 2016  

