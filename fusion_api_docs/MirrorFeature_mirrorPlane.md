# MirrorFeature.mirrorPlane Property

Parent Object: [MirrorFeature](MirrorFeature.md)  

## Description

Gets and sets the mirror plane. This can be either a planar face or construction plane. This works only for parametric features.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"mirrorFeature_var" is a variable referencing a MirrorFeature object.  

```python
# Get the value of the property.
propertyValue = mirrorFeature_var.mirrorPlane

# Set the value of the property.
mirrorFeature_var.mirrorPlane = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version November 2014  

