# StitchFeature.stitchSurfaces Property

Parent Object: [StitchFeature](StitchFeature.md)  

## Description

Gets and sets the surfaces to stitch together. In some cases the stitch operation results in faces being merged so the original faces are no longer available after the feature is created. in this case you need to reposition the timeline marker to just before this feature when the faces do exist.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"stitchFeature_var" is a variable referencing a StitchFeature object.  

```python
# Get the value of the property.
propertyValue = stitchFeature_var.stitchSurfaces

# Set the value of the property.
stitchFeature_var.stitchSurfaces = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

