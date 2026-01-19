# DraftFeature.plane Property

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Gets and sets the plane that defines the direction in which the draft is applied. This is also referred to as the pull direction. This can be defined using either a planar BrepFace, or a ConstructionPlane.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"draftFeature_var" is a variable referencing a DraftFeature object.  

```python
# Get the value of the property.
propertyValue = draftFeature_var.plane

# Set the value of the property.
draftFeature_var.plane = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version January 2015  

