# MoveFeaturePointToPositionDefinition.isDesignSpace Property

Parent Object: [MoveFeaturePointToPositionDefinition](MoveFeaturePointToPositionDefinition.md)  

## Description

Gets and sets if the translation is defined with respect to the design or component space. Design space is the same as the root component space.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeaturePointToPositionDefinition_var" is a variable referencing a MoveFeaturePointToPositionDefinition object.  

```python
# Get the value of the property.
propertyValue = moveFeaturePointToPositionDefinition_var.isDesignSpace

# Set the value of the property.
moveFeaturePointToPositionDefinition_var.isDesignSpace = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2023  

