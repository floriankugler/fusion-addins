# PatchFeature.interiorRailsAndPoints Property

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

Gets and sets any interior curves or points the patch should fit through. Valid entities include object collections of connected curves, paths, sketch curves, sketch points, B-Rep edges, and construction points.  

When getting this property, the returned ObjectCollection can contain individual edges, sketch curves, sketch points, construction points, vertices, and ObjectCollection objects that represent a group of the curves and points listed above.  

Can be set to null to remove any interior rails and points from the patch.  

To get or set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"patchFeature_var" is a variable referencing a PatchFeature object.  

```python
# Get the value of the property.
propertyValue = patchFeature_var.interiorRailsAndPoints

# Set the value of the property.
patchFeature_var.interiorRailsAndPoints = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2022  

