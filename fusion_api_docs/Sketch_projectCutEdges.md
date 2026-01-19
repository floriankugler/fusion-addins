# Sketch.projectCutEdges Method

Parent Object: [Sketch](Sketch.md)  

## Description

Intersects the specified body with the sketch plane and creates new curves representing the intersection.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.projectCutEdges(body)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns a collection of the sketch entities that were created a a result of the cut. |

## Parameters

| Name | Type                     | Description                               |
|------|--------------------------|-------------------------------------------|
| body | [BRepBody](BRepBody.md) | The body to be intersected by the sketch. |

## Version

Introduced in version August 2014  

