# TwoDistancesChamferEdgeSet.isFlipped Property

Parent Object: [TwoDistancesChamferEdgeSet](TwoDistancesChamferEdgeSet.md)  

## Description

Gets and sets if the chamfer is flipped. This swaps the directions for distance one and two.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"twoDistancesChamferEdgeSet_var" is a variable referencing a TwoDistancesChamferEdgeSet object.  

```python
# Get the value of the property.
propertyValue = twoDistancesChamferEdgeSet_var.isFlipped

# Set the value of the property.
twoDistancesChamferEdgeSet_var.isFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version December 2020  

