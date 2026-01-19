# MirrorFeature.isCombine Property

Parent Object: [MirrorFeature](MirrorFeature.md)  

## Description

Gets and sets whether combine is set when doing the Mirror. When true, the mirrored geometry will be Boolean unioned with the original solid or surface body(s) when they connect within the stitch tolerance defined with the stitchTolerance property. If the bodies cannot be unioned or stitched the result will be separate bodies.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"mirrorFeature_var" is a variable referencing a MirrorFeature object.  

```python
# Get the value of the property.
propertyValue = mirrorFeature_var.isCombine

# Set the value of the property.
mirrorFeature_var.isCombine = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2020  

