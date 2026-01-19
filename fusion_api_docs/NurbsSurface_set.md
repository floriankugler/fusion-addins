# NurbsSurface.set Method

Parent Object: [NurbsSurface](NurbsSurface.md)  

## Description

Sets the data that defines the NURBS surface.

## Syntax

"nurbsSurface_var" is a variable referencing a [NurbsSurface](NurbsSurface.md) object.

```python
returnValue = nurbsSurface_var.set(degreeU, degreeV, controlPointCountU, controlPointCountV, controlPoints, knotsU, knotsV, weights, propertiesU, propertiesV)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| degreeU | integer | The degree in the U direction. |
| degreeV | integer | The degree in the V direction. |
| controlPointCountU | integer | The number of control points in the U direction. |
| controlPointCountV | integer | The number of control points in the V direction. |
| controlPoints | Point3D\[\] | An array of surface control points. |
| knotsU | double\[\] | The knot vector for the U direction. |
| knotsV | double\[\] | The knot vector for the V direction. |
| weights | double\[\] | An array of weights that corresponds to the control points of the surface. |
| propertiesU | [NurbsSurfaceProperties](NurbsSurfaceProperties.md) | The properties (NurbsSurfaceProperties) of the surface in the U direction. |
| propertiesV | [NurbsSurfaceProperties](NurbsSurfaceProperties.md) | The properties (NurbsSurfaceProperties) of the surface in the V direction. |

## Version

Introduced in version August 2014  

