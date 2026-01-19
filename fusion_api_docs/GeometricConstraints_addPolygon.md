# GeometricConstraints.addPolygon Method

Parent Object: [GeometricConstraints](GeometricConstraints.md)  

## Description

Creates a polygon constraint on existing lines in the sketch.

## Syntax

"geometricConstraints_var" is a variable referencing a [GeometricConstraints](GeometricConstraints.md) object.

```python
returnValue = geometricConstraints_var.addPolygon(lines)
```

## Return Value

| Type | Description |
|----|----|
| [PolygonConstraint](PolygonConstraint.md) | Returns the created PolygonConstraint or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| lines | SketchLine\[\] | An array of existing SketchLine objects in this sketch that define a valid polygon. They must be the same length, connect at their endpoints, have the same angle between them, and define a closed shape. The order of the lines within the array does not matter. |

## Version

Introduced in version January 2025  

