# Sketch.intersectWithSketchPlane Method

Parent Object: [Sketch](Sketch.md)  

## Description

Intersects the specified entities (BRepBody, BRepFace, BRepEdge, BRepVertex, SketchCurve, ConstructionPoint, ConstructionAxis, and ConstructionPlane) with the sketch plane and creates sketch geometry that represents the intersection.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.intersectWithSketchPlane(entities)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEntity](SketchEntity.md)\[\] | An array returning the sketch entities that were created as a result of the intersections. It's possible that this can come back empty in the case where the input entities don't intersect the sketch plane. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | Base\[\] | An array containing the entities to intersect with the sketch plane. |

## Samples

| Name | Description |
|----|----|
| [Sketch Intersect API Sample](SketchIntersect_Sample.md) | Intersects the specified entities with the sketch plane and creates sketch geometry that represents the intersection. |

## Version

Introduced in version August 2017  

