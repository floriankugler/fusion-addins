# VariableRadiusFilletEdgeSetInput.continuity Property

Parent Object: [VariableRadiusFilletEdgeSetInput](VariableRadiusFilletEdgeSetInput.md)  

## Description

Gets and sets the continuity of the fillet edge set. Valid values are TangentSurfaceContinuityType and CurvatureSurfaceContinuityType. The default is TangentSurfaceContinuityType.  

For an asymmetric fillet edge set, this must always be tangent continuity (G1) and setting it to another value will fail.

## Syntax

"variableRadiusFilletEdgeSetInput_var" is a variable referencing a VariableRadiusFilletEdgeSetInput object.  

```python
# Get the value of the property.
propertyValue = variableRadiusFilletEdgeSetInput_var.continuity

# Set the value of the property.
variableRadiusFilletEdgeSetInput_var.continuity = propertyValue
```

## Property Value

This is a read/write property whose value is a [SurfaceContinuityTypes](SurfaceContinuityTypes.md).

## Version

Introduced in version November 2022  

