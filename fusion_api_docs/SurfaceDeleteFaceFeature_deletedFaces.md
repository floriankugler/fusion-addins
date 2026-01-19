# SurfaceDeleteFaceFeature.deletedFaces Property

Parent Object: [SurfaceDeleteFaceFeature](SurfaceDeleteFaceFeature.md)  

## Description

Gets and sets the set of faces that are deleted by this feature.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"surfaceDeleteFaceFeature_var" is a variable referencing a SurfaceDeleteFaceFeature object.  

```python
# Get the value of the property.
propertyValue = surfaceDeleteFaceFeature_var.deletedFaces

# Set the value of the property.
surfaceDeleteFaceFeature_var.deletedFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version August 2016  

