# FilletEdgeSetInput.continuity Property

Parent Object: [FilletEdgeSetInput](FilletEdgeSetInput.md)  

## Description

Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. The default is TangentSurfaceContinuityType.  

For an asymmetric fillet edge set, this must always be tangent continuity (G1) and setting it to another value will fail.

## Syntax

"filletEdgeSetInput_var" is a variable referencing a FilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = filletEdgeSetInput_var.continuity

# Set the value of the property.
filletEdgeSetInput_var.continuity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceContinuityTypes](SurfaceContinuityTypes.md).

## Version

Introduced in version November 2022  

