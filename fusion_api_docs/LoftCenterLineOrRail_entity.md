# LoftCenterLineOrRail.entity Property

Parent Object: [LoftCenterLineOrRail](LoftCenterLineOrRail.md)  

## Description

Gets and sets the entity that defines the centerline or rail. This can be a single sketch entity, a single BRepEdge, a Path, or a Profile.  

If this LoftCenterLineOrRail object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftCenterLineOrRail_var" is a variable referencing a LoftCenterLineOrRail object.  

```python
# Get the value of the property.
propertyValue = loftCenterLineOrRail_var.entity

# Set the value of the property.
loftCenterLineOrRail_var.entity = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version August 2016  

