# DistanceAndAngleChamferEdgeSet.isFlipped Property

Parent Object: [DistanceAndAngleChamferEdgeSet](DistanceAndAngleChamferEdgeSet.md)  

## Description

Gets and sets if the chamfer is flipped. This swaps the directions for distance one and two.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"distanceAndAngleChamferEdgeSet_var" is a variable referencing a DistanceAndAngleChamferEdgeSet object.  

```python
# Get the value of the property.
propertyValue = distanceAndAngleChamferEdgeSet_var.isFlipped

# Set the value of the property.
distanceAndAngleChamferEdgeSet_var.isFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version December 2020  

