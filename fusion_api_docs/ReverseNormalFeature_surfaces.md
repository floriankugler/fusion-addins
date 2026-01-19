# ReverseNormalFeature.surfaces Property

Parent Object: [ReverseNormalFeature](ReverseNormalFeature.md)  

## Description

Gets and sets the surface bodies (open BRepBodies) whose faces normals are to be reversed. All faces of the input surface bodies get reversed.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"reverseNormalFeature_var" is a variable referencing a ReverseNormalFeature object.  

```python
# Get the value of the property.
propertyValue = reverseNormalFeature_var.surfaces

# Set the value of the property.
reverseNormalFeature_var.surfaces = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2015  

