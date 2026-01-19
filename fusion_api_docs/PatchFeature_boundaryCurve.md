# PatchFeature.boundaryCurve Property

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Returns an ObjectCollection that contains all of the sketch curves or B-Rep edges that defines the closed outer boundary of the patch feature.  

When setting this property, the input can be a sketch profile, a single sketch curve, a single B-Rep edge, or an ObjectCollection of sketch curves and B-Rep edges.  

If a single open sketch curve or B-Rep edge is input, Fusion will automatically find connected sketch curves or B-Rep edges to define a closed loop.  

If an ObjectCollection of sketch curves or B-Rep edges is input, they must define a closed shape.  

To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"patchFeature_var" is a variable referencing a PatchFeature object.  

```python
# Get the value of the property.
propertyValue = patchFeature_var.boundaryCurve

# Set the value of the property.
patchFeature_var.boundaryCurve = propertyValue
```

## Property Value

This is a read/write property whose value is a [Base](Base.md).

## Version

Introduced in version July 2016  

