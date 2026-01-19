# SplitFaceFeature.facesToSplit Property

Parent Object: [SplitFaceFeature](SplitFaceFeature.md)  

## Description

Gets and sets the faces to be split. The collection can contain one or more faces selected from solid and/or open bodies.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitFaceFeature_var" is a variable referencing a SplitFaceFeature object.  

```python
# Get the value of the property.
propertyValue = splitFaceFeature_var.facesToSplit

# Set the value of the property.
splitFaceFeature_var.facesToSplit = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

