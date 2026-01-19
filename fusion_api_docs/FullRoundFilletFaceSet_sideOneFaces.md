# FullRoundFilletFaceSet.sideOneFaces Property

Parent Object: [FullRoundFilletFaceSet](FullRoundFilletFaceSet.md)  

## Description

Gets the side one faces.  

When this face set is associated with an existing fillet feature, to get the side one faces you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"fullRoundFilletFaceSet_var" is a variable referencing a FullRoundFilletFaceSet object.  

```python
# Get the value of the property.
propertyValue = fullRoundFilletFaceSet_var.sideOneFaces
```

## Property Value

This is a read only property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version September 2025  

