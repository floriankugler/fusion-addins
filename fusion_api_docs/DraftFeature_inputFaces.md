# DraftFeature.inputFaces Property

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Gets and sets the input faces. If isTangentChain is true, all the faces that are tangentially connected to the input faces (if any) will also be included.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"draftFeature_var" is a variable referencing a DraftFeature object.  

```python
# Get the value of the property.
propertyValue = draftFeature_var.inputFaces

# Set the value of the property.
draftFeature_var.inputFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version January 2015  

