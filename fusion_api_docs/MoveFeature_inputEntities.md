# MoveFeature.inputEntities Property

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Gets and sets the entities to move. This is done by using an ObjectCollection containing the objects to move. For a parametric model, the collection can contain BRepBody or BRepFace objects but not a combination of both.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a MoveFeature object.  

```python
# Get the value of the property.
propertyValue = moveFeature_var.inputEntities

# Set the value of the property.
moveFeature_var.inputEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version March 2015  

