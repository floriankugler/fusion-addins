# MoveFeaturePointToPositionDefinition.point Property

Parent Object: [MoveFeaturePointToPositionDefinition](MoveFeaturePointToPositionDefinition.md)  

## Description

Gets and sets the entity that defines a point in space. This can be a sketch point, a construction point, or a BRepVertex.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeaturePointToPositionDefinition_var" is a variable referencing a MoveFeaturePointToPositionDefinition object.  

```python
# Get the value of the property.
propertyValue = moveFeaturePointToPositionDefinition_var.point

# Set the value of the property.
moveFeaturePointToPositionDefinition_var.point = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version January 2023  

