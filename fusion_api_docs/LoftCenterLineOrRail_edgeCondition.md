# LoftCenterLineOrRail.edgeCondition Property

Parent Object: [LoftCenterLineOrRail](LoftCenterLineOrRail.md)  

## Description

Gets and sets the edge condition for this rail. This value is only applicable when a BRepEdge is used as the rail entity. If sketch geometry is used, this value is ignored. The property defaults to G0LoftRailEdgeCondition.  

If this LoftCenterLineOrRail object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftCenterLineOrRail_var" is a variable referencing a LoftCenterLineOrRail object.  

```python
# Get the value of the property.
propertyValue = loftCenterLineOrRail_var.edgeCondition

# Set the value of the property.
loftCenterLineOrRail_var.edgeCondition = propertyValue
```

## Property Value

This is a read/write property whose value is a [LoftRailEdgeConditions](LoftRailEdgeConditions.md).

## Version

Introduced in version November 2022  

