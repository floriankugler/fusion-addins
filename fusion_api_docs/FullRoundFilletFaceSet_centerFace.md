# FullRoundFilletFaceSet.centerFace Property

Parent Object: [FullRoundFilletFaceSet](FullRoundFilletFaceSet.md)  

## Description

Gets the center face associated with this full round fillet face set. When a center face has tangentially connected faces then all the tangentially connected faces will be filleted automatically.  

When this face set is associated with an existing fillet feature, to get the center face you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"fullRoundFilletFaceSet_var" is a variable referencing a FullRoundFilletFaceSet object.  

```python
# Get the value of the property.
propertyValue = fullRoundFilletFaceSet_var.centerFace
```

## Property Value

This is a read only property whose value is a [BRepFace](BRepFace.md).

## Version

Introduced in version September 2025  

