# PatchFeature.continuity Property

Parent Object: [PatchFeature](PatchFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the type of surface continuity used when creating the patch face. This value is only used when BRepEdges are input and defines the continuity of how the patch face connects to the face adjacent to each of the input edges.  

To set this property, you need to position the timeline marker immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Remarks

This property has been retired and replaced by either the groupContinuity property or setContinuity method, depending on if the isGroupEdges property is true or not.

## Syntax

"patchFeature_var" is a variable referencing a PatchFeature object.  

```python
# Get the value of the property.
propertyValue = patchFeature_var.continuity

# Set the value of the property.
patchFeature_var.continuity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceContinuityTypes](SurfaceContinuityTypes.md).

## Version

Introduced in version July 2016  
Retired in version November 2022  

