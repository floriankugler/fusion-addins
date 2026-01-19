# MoveFeatureFreeMoveDefinition.transform Property

Parent Object: [MoveFeatureFreeMoveDefinition](MoveFeatureFreeMoveDefinition.md)  

## Description

Gets and sets the transform that's applied to the face or body. The matrix must be an orthogonal matrix; that is the axes are perpendicular to each other and there isn't any scaling or mirroring defined.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeatureFreeMoveDefinition_var" is a variable referencing a MoveFeatureFreeMoveDefinition object.  

```python
# Get the value of the property.
propertyValue = moveFeatureFreeMoveDefinition_var.transform

# Set the value of the property.
moveFeatureFreeMoveDefinition_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version January 2023  

