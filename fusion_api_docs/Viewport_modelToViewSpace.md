# Viewport.modelToViewSpace Method

Parent Object: [Viewport](Viewport.md)  

## Description

A specified point in model space returns the equivalent point in view space.

## Syntax

"viewport_var" is a variable referencing a [Viewport](Viewport.md) object.

```python
returnValue = viewport_var.modelToViewSpace(modelCoordinate)
```

## Return Value

| Type                   | Description                                 |
|------------------------|---------------------------------------------|
| [Point2D](Point2D.md) | Returns the equivalent point in view space. |

## Parameters

| Name            | Type                   | Description                  |
|-----------------|------------------------|------------------------------|
| modelCoordinate | [Point3D](Point3D.md) | A coordinate in model space. |

## Version

Introduced in version December 2016  

