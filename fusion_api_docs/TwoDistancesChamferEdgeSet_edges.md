# TwoDistancesChamferEdgeSet.edges Property

Parent Object: [TwoDistancesChamferEdgeSet](TwoDistancesChamferEdgeSet.md)  

## Description

Gets and sets the edges that will be chamfered. This collection can contain BRepEdge, BRepFace, and Feature objects. If BRepFace or Feature are objects are provided, all of the edges associated with those objects will be chamfered.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"twoDistancesChamferEdgeSet_var" is a variable referencing a TwoDistancesChamferEdgeSet object.  

```python
# Get the value of the property.
propertyValue = twoDistancesChamferEdgeSet_var.edges

# Set the value of the property.
twoDistancesChamferEdgeSet_var.edges = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version December 2020  

