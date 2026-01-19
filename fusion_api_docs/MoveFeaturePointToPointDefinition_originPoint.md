# MoveFeaturePointToPointDefinition.originPoint Property

Parent Object: [MoveFeaturePointToPointDefinition](MoveFeaturePointToPointDefinition.md)  

## Description

Gets and sets the first point that defines the start position of the move.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeaturePointToPointDefinition_var" is a variable referencing a MoveFeaturePointToPointDefinition object.  

```python
# Get the value of the property.
propertyValue = moveFeaturePointToPointDefinition_var.originPoint

# Set the value of the property.
moveFeaturePointToPointDefinition_var.originPoint = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version January 2023  

