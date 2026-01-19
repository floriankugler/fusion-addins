# PatchFeatureInput.groupContinuity Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

Gets and sets the type of surface continuity to use for all edges when the isGroupEdges property is true. The continuity is used to determine how the patch connects to any B-Rep edges in the boundary. It is ignored for any sketch curves in the boundary. The property defaults to ConnectedSurfaceContinuityType. The value of this property is ignored if the isGroupEdges property is false.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.groupContinuity

# Set the value of the property.
patchFeatureInput_var.groupContinuity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceContinuityTypes](SurfaceContinuityTypes.md).

## Version

Introduced in version November 2022  

