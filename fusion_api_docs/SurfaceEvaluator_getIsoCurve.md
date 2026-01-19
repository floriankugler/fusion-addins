# SurfaceEvaluator.getIsoCurve Method

Parent Object: [SurfaceEvaluator](SurfaceEvaluator.md)  

## Description

Gets (by extraction) a curve that follows a constant u or v parameter along the surface. The curve will have the same properties as the surface in the direction of the extraction. For example, when a curve is extracted from the periodic direction of a surface, the extracted curve will also be periodic. The type of curve returned is dependent on the shape the surface.  

Getting an iso curve is limited to a SurfaceEvaluator that is obtained from a BRepFace. It will fail when the SurfaceEvaluator is obtained from a geometry object (Plane, Sphere, Torus, Cylinder, Cone, EllipticalCone, EllipticalCylinder, or NurbsSurface).

## Syntax

"surfaceEvaluator_var" is a variable referencing a [SurfaceEvaluator](SurfaceEvaluator.md) object.

```python
returnValue = surfaceEvaluator_var.getIsoCurve(parameter, isUDirection)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | Returns an ObjectCollection that contains one or more curves. Multiple curves are returned when the SurfaceEvaluator is obtained from a Face and the curve cuts across internal boundaries. The resulting curves are trimmed to the boundaries of the Face. When the SurfaceEvaluator is obtained from a geometry object, a single curve is returned because there are no boundaries to trim the curve. The type of curve(s) returned is dependent on the shape of the surface. |

## Parameters

| Name | Type | Description |
|----|----|----|
| parameter | double | The parameter at which to extract the curve |
| isUDirection | boolean | A bool that indicates whether to extract the curve from the U or V direction |

## Version

Introduced in version August 2014  

