# MoveFeatureTranslateAlongEntityDefinition.linearEntity Property

Parent Object: [MoveFeatureTranslateAlongEntityDefinition](MoveFeatureTranslateAlongEntityDefinition.md)  

## Description

Gets and sets the linear entity that defines the direction of the move. This can be a linear BRepEdge, ConstructionAxis, or a SketchLine. The entity defines the direction, not the distance. The natural direction of the entity defines the translation direction.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeatureTranslateAlongEntityDefinition_var" is a variable referencing a MoveFeatureTranslateAlongEntityDefinition object.  

```python
# Get the value of the property.
propertyValue = moveFeatureTranslateAlongEntityDefinition_var.linearEntity

# Set the value of the property.
moveFeatureTranslateAlongEntityDefinition_var.linearEntity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version January 2023  

