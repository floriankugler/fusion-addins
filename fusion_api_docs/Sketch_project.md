# Sketch.project Method

Parent Object: [Sketch](Sketch.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

This method has been replaced by the project2 method, which supports specifying if the result will be linked or not.

## Remarks

Projects the specified entity or entities onto the x-y plane of the sketch and returns the created sketch entity(s). You can provide either a single entity or an ObjectCollection of multiple entities, which will be projected simultaneously.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.project(entity)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns a collection of the sketch entities that were created as a result of the projection. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| entity | [Base](Base.md) | The entity to project. This can be a single entity of the following types: sketch entity, an edge, a face (which will get all of its edges), a vertex, a construction axis, a construction point, or a construction plane that is perpendicular to the sketch to create a line. This can also be an ObjectCollection that contains multiple entities and will be projected simultaneously. The entities that can be projected must be the types and have the same restrictions as described above. |

## Version

Introduced in version August 2014  
Retired in version May 2025  

