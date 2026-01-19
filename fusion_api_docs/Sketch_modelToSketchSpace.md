# Sketch.modelToSketchSpace Method

Parent Object: [Sketch](Sketch.md)  

## Description

A specified point in model space returns the equivalent point in sketch space. This is sensitive to the assembly context.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.modelToSketchSpace(modelCoordinate)
```

## Return Value

| Type                   | Description                                   |
|------------------------|-----------------------------------------------|
| [Point3D](Point3D.md) | Returns the equivalent point in sketch space. |

## Parameters

| Name            | Type                   | Description                  |
|-----------------|------------------------|------------------------------|
| modelCoordinate | [Point3D](Point3D.md) | A coordinate in model space. |

## Version

Introduced in version August 2014  

