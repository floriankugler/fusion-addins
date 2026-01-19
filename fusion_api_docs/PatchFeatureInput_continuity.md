# PatchFeatureInput.continuity Property

Parent Object: [PatchFeatureInput](PatchFeatureInput.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the type of surface continuity to use when matching boundary edges to face edges. When a new PatchFeatureInput is created, this is initialized to ConnectedSurfaceContinuityType. This value is ignored when creating a patch for sketch curves.

## Remarks

This property has been retired and replaced by either the groupContinuity property or setContinuity method, depending on if the isGroupEdges property is true or not.

## Syntax

"patchFeatureInput_var" is a variable referencing a PatchFeatureInput object.  

```python
# Get the value of the property.
propertyValue = patchFeatureInput_var.continuity

# Set the value of the property.
patchFeatureInput_var.continuity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceContinuityTypes](SurfaceContinuityTypes.md).

## Version

Introduced in version July 2016  
Retired in version November 2022  

