# PatchFeature.groupIsContinuityDirectionFlipped Property

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Gets and sets the continuity direction for all edges when the isGroupEdges property is true. It is ignored for any sketch curves in the boundary. The property defaults to false. The value of this property is ignored if the isGroupEdges property is false.  

To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"patchFeature_var" is a variable referencing a PatchFeature object.  

```python
# Get the value of the property.
propertyValue = patchFeature_var.groupIsContinuityDirectionFlipped

# Set the value of the property.
patchFeature_var.groupIsContinuityDirectionFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2022  

