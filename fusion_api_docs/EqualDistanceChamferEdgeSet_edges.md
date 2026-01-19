# EqualDistanceChamferEdgeSet.edges Property

Parent Object: [EqualDistanceChamferEdgeSet](EqualDistanceChamferEdgeSet.md)  

## Description

Gets and sets the edges that will be chamfered. This collection can contain BRepEdge, BRepFace, and Feature objects. If BRepFace or Feature are objects are provided, all of the edges associated with those objects will be chamfered.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"equalDistanceChamferEdgeSet_var" is a variable referencing an EqualDistanceChamferEdgeSet object.  

```python
# Get the value of the property.
propertyValue = equalDistanceChamferEdgeSet_var.edges

# Set the value of the property.
equalDistanceChamferEdgeSet_var.edges = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version December 2020  

