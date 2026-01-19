# NurbsSurface.getData Method

Parent Object: [NurbsSurface](NurbsSurface.md)  

## Description

Gets the data that defines the NURBS surface.

## Syntax

"nurbsSurface_var" is a variable referencing a [NurbsSurface](NurbsSurface.md) object.  

```python
(returnValue, degreeU, degreeV, controlPointCountU, controlPointCountV, controlPoints, knotsU, knotsV, weights, propertiesU, propertiesV) = nurbsSurface_var.getData()
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| degreeU | integer | The output degree in the U direction. |
| degreeV | integer | The output degree in the V direction. |
| controlPointCountU | integer | The output number of control points in the U direction. |
| controlPointCountV | integer | The output number of control points in the V direction. |
| controlPoints | Point3D\[\] | An output array of surface control points. |
| knotsU | double\[\] | The output knot vector for the U direction. |
| knotsV | double\[\] | The output knot vector for the V direction. |
| weights | double\[\] | An output array of weights that corresponds to the control points of the surface. |
| propertiesU | [NurbsSurfaceProperties](NurbsSurfaceProperties.md) | The output properties (NurbsSurfaceProperties) of the surface in the U direction. |
| propertiesV | [NurbsSurfaceProperties](NurbsSurfaceProperties.md) | The output properties (NurbsSurfaceProperties) of the surface in the V direction. |

## Version

Introduced in version August 2014  

