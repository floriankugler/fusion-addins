# DeleteFaceFeature.deletedFaces Property

Parent Object: [DeleteFaceFeature](DeleteFaceFeature.md)  

## Description

Gets and sets the set of faces that are deleted by this feature.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

Setting this property can fail if Fusion is unable to heal the body after deleting the specified faces.

## Syntax

"deleteFaceFeature_var" is a variable referencing a DeleteFaceFeature object.  

```python
# Get the value of the property.
propertyValue = deleteFaceFeature_var.deletedFaces

# Set the value of the property.
deleteFaceFeature_var.deletedFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version August 2016  

