# BRepFace.evaluator Property

Parent Object: [BRepFace](BRepFace.md)  

## Description

Returns a SurfaceEvaluator to allow geometric evaluations across the face's surface. This evaluator differs from the evaluator available from the Surface obtained from the geometry property by being bounded by the topological boundaries of this face.

## Syntax

"bRepFace_var" is a variable referencing a BRepFace object.  

```python
# Get the value of the property.
propertyValue = bRepFace_var.evaluator
```

## Property Value

This is a read only property whose value is a [SurfaceEvaluator](SurfaceEvaluator.md).

## Version

Introduced in version August 2014  

