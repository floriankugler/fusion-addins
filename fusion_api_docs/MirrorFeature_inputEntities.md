# MirrorFeature.inputEntities Property

Parent Object: [MirrorFeature](MirrorFeature.md)  

## Description

Gets and sets the entities that are mirrored. It can contain faces, features, bodies, or components. The input must all be of a single type. For example, you can't provide a body and a component but the collection must be either all bodies or all components.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"mirrorFeature_var" is a variable referencing a MirrorFeature object.  

```python
# Get the value of the property.
propertyValue = mirrorFeature_var.inputEntities

# Set the value of the property.
mirrorFeature_var.inputEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2014  

