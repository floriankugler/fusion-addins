# MoveFeatureRotateDefinition.axisEntity Property

Parent Object: [MoveFeatureRotateDefinition](MoveFeatureRotateDefinition.md)  

## Description

Gets and sets the linear entity that defines the axis of rotation. This can be a linear BRepEdge, ConstructionAxis, or a SketchLine. The natural direction of the entity defines a right-hand rule for the rotation direction.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeatureRotateDefinition_var" is a variable referencing a MoveFeatureRotateDefinition object.  

```python
# Get the value of the property.
propertyValue = moveFeatureRotateDefinition_var.axisEntity

# Set the value of the property.
moveFeatureRotateDefinition_var.axisEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version January 2023  

