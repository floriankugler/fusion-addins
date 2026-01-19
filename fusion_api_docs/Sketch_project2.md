# Sketch.project2 Method

Parent Object: [Sketch](Sketch.md)  

## Description

Projects the specified entity or entities onto the X-Y plane of the sketch and returns the created sketch entity(s).

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.project2(entities, isLinked)
```

## Return Value

| Type | Description |
|----|----|
| [SketchEntity](SketchEntity.md)\[\] | Returns an array of the sketch entities that were created as a result of the projection. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entities | Base\[\] | An array containing the entities to project. It can be an array of one for the case where a single entity is being projected. The following types of entities are valid for projection: sketch curves and points, B-Rep bodies (which results in projecting the silhouette of the body), B-Rep edges, B-Rep faces (which results in projecting all of its edges), B-Rep vertices, construction axes, construction points, and construction planes that are perpendicular to the sketch which results in the creation of a line. |
| isLinked | boolean | A Boolean that indicates if the resulting sketch curves will be parametrically linked to the source geometry that was projected. If true, they will be linked. If false, the resulting curves are independent. |

## Version

Introduced in version May 2025  

