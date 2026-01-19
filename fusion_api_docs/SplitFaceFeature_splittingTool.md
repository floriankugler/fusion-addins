# SplitFaceFeature.splittingTool Property

Parent Object: [SplitFaceFeature](SplitFaceFeature.md)  

## Description

Gets the entity(s) that define the splitting tool(s). The splitting tool can consist of one or more of the following: BRepBody, ConstructionPlane, BRepFace, sketch curve that extends or can be extended beyond the extents of the face. To set the splitting tool, use one of the set methods to also define the split type.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitFaceFeature_var" is a variable referencing a SplitFaceFeature object.  

```python
# Get the value of the property.
propertyValue = splitFaceFeature_var.splittingTool
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

