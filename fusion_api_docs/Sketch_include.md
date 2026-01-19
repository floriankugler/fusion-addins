# Sketch.include Method

Parent Object: [Sketch](Sketch.md)  

## Description

Creates new sketch curves and points that represent the specified entity as sketch geometry. The sketch geometry is not projected but is created in the same location in space as the input geometry.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.include(entity)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns a collection of the sketch entities that were created as a result of the include. When including this curves it will be a single sketch curve, but for faces, multiple sketch curves will be created; one for each edge. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | The entity to include into the sketch. This can be a sketch entity from another sketch, edge, face (which results in getting all of its edges, a vertex, construction axis, or construction point. |

## Version

Introduced in version August 2014  

