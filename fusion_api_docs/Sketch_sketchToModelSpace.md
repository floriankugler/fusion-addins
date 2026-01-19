# Sketch.sketchToModelSpace Method

Parent Object: [Sketch](Sketch.md)  

## Description

A specified point in sketch space returns the equivalent point in model space. This is sensitive to the assembly context.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.sketchToModelSpace(sketchCoordinate)
```

## Return Value

| Type                   | Description                                  |
|------------------------|----------------------------------------------|
| [Point3D](Point3D.md) | Returns the equivalent point in model space. |

## Parameters

| Name             | Type                   | Description                   |
|------------------|------------------------|-------------------------------|
| sketchCoordinate | [Point3D](Point3D.md) | A coordinate in sketch space. |

## Version

Introduced in version August 2014  

