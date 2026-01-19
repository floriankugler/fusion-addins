# PatchFeatureInput.interiorRailsAndPoints Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

Gets and sets any interior curves or points the patch should fit through. Valid entities include object collections of connected curves, paths, sketch curves, sketch points, B-Rep edges, and construction points.  

When getting this property, the returned ObjectCollection can contain individual edges, sketch curves, sketch points, construction points, vertices, and ObjectCollection objects that represent a group of the curves and points listed above.  

Can be set to null to remove any interior rails and points from the patch.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.interiorRailsAndPoints

# Set the value of the property.
patchFeatureInput_var.interiorRailsAndPoints = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2022  

