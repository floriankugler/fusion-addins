# LoftSection.entity Property

Parent Object: [LoftSection](LoftSection.md)  

## Description

Get and sets the entity that defines the section of the loft. This can be a BRepFace, Profile, Path, SketchPoint, ConstructionPoint, or an ObjectCollection of contiguous profiles.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a LoftSection object.  

```python
# Get the value of the property.
propertyValue = loftSection_var.entity

# Set the value of the property.
loftSection_var.entity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version August 2016  

