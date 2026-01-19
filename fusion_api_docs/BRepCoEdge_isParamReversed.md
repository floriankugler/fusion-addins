# BRepCoEdge.isParamReversed Property

Parent Object: [BRepCoEdge](BRepCoEdge.md)  

## Description

Returns if the parametric direction of this co-edge is reversed from the parametric direction of the underlying curve obtained from the geometry property. A co-edge's parametric direction is from the start vertex to the end vertex. But the underlying curve geometry may have the opposite parameterization. This property indicates if the parameterization order of the evaluator obtained from this co-edge is reversed from the order of the geometry curve's evaluator.

## Syntax

"bRepCoEdge_var" is a variable referencing a BRepCoEdge object.  

```python
# Get the value of the property.
propertyValue = bRepCoEdge_var.isParamReversed
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version August 2014  

