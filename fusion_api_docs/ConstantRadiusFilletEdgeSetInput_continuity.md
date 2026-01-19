# ConstantRadiusFilletEdgeSetInput.continuity Property

Parent Object: [ConstantRadiusFilletEdgeSetInput](ConstantRadiusFilletEdgeSetInput.md)  

## Description

Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. The default is TangentSurfaceContinuityType.  

For an asymmetric fillet edge set, this must always be tangent continuity (G1) and setting it to another value will fail.

## Syntax

"constantRadiusFilletEdgeSetInput_var" is a variable referencing a ConstantRadiusFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = constantRadiusFilletEdgeSetInput_var.continuity

# Set the value of the property.
constantRadiusFilletEdgeSetInput_var.continuity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceContinuityTypes](SurfaceContinuityTypes.md).

## Samples

| Name | Description |
|----|----|
| [Fillet Feature API Sample](FilletFeatureSample_Sample.md) | Demonstrates creating fillets using the various types of fillets. Create a new design and add a box that is at least 2 cm on each side. The script creates a constant radius, variable radius and chord length fillets. After creating each one, it deletes it and then creates the next. To see any of the fillets that were deleted, undo to get the fillet back. |

## Version

Introduced in version November 2022  

