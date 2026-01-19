# SurfaceEvaluator Object

Derived from: [Base](Base.md) Object  

## Description

Surface evaluator that is obtained from a transient surface and allows you to perform various evaluations on the surface.

## Methods

| Name | Description |
| --- | --- |
| [classType](SurfaceEvaluator_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getCurvature](SurfaceEvaluator_getCurvature.md) | Get the curvature values at a parameter positions on the surface. |
| [getCurvatures](SurfaceEvaluator_getCurvatures.md) | Get the curvature values at a number of parameter positions on the surface. |
| [getFirstDerivative](SurfaceEvaluator_getFirstDerivative.md) | Get the first derivative of the surface at the specified parameter position. |
| [getFirstDerivatives](SurfaceEvaluator_getFirstDerivatives.md) | Get the first derivatives of the surface at the specified parameter positions. |
| [getIsoCurve](SurfaceEvaluator_getIsoCurve.md) | Gets (by extraction) a curve that follows a constant u or v parameter along the surface. The curve will have the same properties as the surface in the direction of the extraction. For example, when a curve is extracted from the periodic direction of a surface, the extracted curve will also be periodic. The type of curve returned is dependent on the shape the surface. Getting an iso curve is limited to a SurfaceEvaluator that is obtained from a BRepFace. It will fail when the SurfaceEvaluator is obtained from a geometry object (Plane, Sphere, Torus, Cylinder, Cone, EllipticalCone, EllipticalCylinder, or NurbsSurface). |
| [getModelCurveFromParametricCurve](SurfaceEvaluator_getModelCurveFromParametricCurve.md) | Creates the 3D equivalent curve in model space, of a 2D curve defined in the parametric space of the surface. |
| [getNormalAtParameter](SurfaceEvaluator_getNormalAtParameter.md) | Gets the surface normal at a parameter position on the surface. |
| [getNormalAtPoint](SurfaceEvaluator_getNormalAtPoint.md) | Gets the surface normal at a point on the surface. |
| [getNormalsAtParameters](SurfaceEvaluator_getNormalsAtParameters.md) | Gets the surface normal at a number of parameter positions on the surface. |
| [getNormalsAtPoints](SurfaceEvaluator_getNormalsAtPoints.md) | Gets the surface normal at a number of positions on the surface. |
| [getParamAnomaly](SurfaceEvaluator_getParamAnomaly.md) | Gets details about anomalies in parameter space of the surface. This includes information about periodic intervals, singularities, or unbounded parameter ranges. |
| [getParameterAtPoint](SurfaceEvaluator_getParameterAtPoint.md) | Get the parameter position that correspond to a point on the surface. For reliable results, the point should lie on the surface within model tolerance. If the point does not lie on the surface, the parameter of the nearest point on the surface will generally be returned. |
| [getParametersAtPoints](SurfaceEvaluator_getParametersAtPoints.md) | Get the parameter positions that correspond to a set of points on the surface. For reliable results, the points should lie on the surface within model tolerance. If the points do not lie on the surface, the parameter of the nearest point on the surface will generally be returned. |
| [getPointAtParameter](SurfaceEvaluator_getPointAtParameter.md) | Get the point on the surface that correspond to evaluating a parameter position on the surface. |
| [getPointsAtParameters](SurfaceEvaluator_getPointsAtParameters.md) | Get the points on the surface that correspond to evaluating a set of parameter positions on the surface. |
| [getSecondDerivative](SurfaceEvaluator_getSecondDerivative.md) | Get the second derivative of the surface at the specified parameter position. |
| [getSecondDerivatives](SurfaceEvaluator_getSecondDerivatives.md) | Get the second derivatives of the surface at the specified parameter positions. |
| [getThirdDerivative](SurfaceEvaluator_getThirdDerivative.md) | Get the third derivative of the surface at the specified parameter position. |
| [getThirdDerivatives](SurfaceEvaluator_getThirdDerivatives.md) | Get the third derivatives of the surface at the specified parameter positions. |
| [isParameterOnFace](SurfaceEvaluator_isParameterOnFace.md) | Determines if the specified parameter position lies within the surface. When the SurfaceEvaluator is obtained from a BRepFace object, this will respect the boundaries of the face and return true when point is on the visible portion of the surface. When obtained from surface geometry it returns true if the point is within the parametric range of surface. |
| [parametricRange](SurfaceEvaluator_parametricRange.md) | Returns the parametric range of the surface. If the surface is periodic in a direction, the range is set to the principle period's range. If the surface is only upper bounded in a direction, the lower bound is set to -double-max. If the surface is only lower bounded in a direction, the upper bound is set to double-max. If the surface is unbounded in a direction, the lower bound and upper bound of the range will both be zero. |

## Properties

| Name | Description |
| --- | --- |
| [area](SurfaceEvaluator_area.md) | Returns the area of the surface. This is typically used when the SurfaceEvaluator is associated with a BRepFace object where it is always valid. This can fail in the case where the SurfaceEvaluator is associated with one of the geometry classes, (Plane, Cylinder, Cone, EllipticalCone, or EllipticalCylinder object), because these surfaces are unbounded. A BRepFace, even one of these shapes, is bounded by its edges and has a well-defined area. |
| [isClosedInU](SurfaceEvaluator_isClosedInU.md) | Returns if the surface is closed (forms a loop) in the U direction |
| [isClosedInV](SurfaceEvaluator_isClosedInV.md) | Returns if the surface is closed (forms a loop) in the V direction |
| [isValid](SurfaceEvaluator_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SurfaceEvaluator_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepFace.evaluator](BRepFace_evaluator.md), [Cone.evaluator](Cone_evaluator.md), [Cylinder.evaluator](Cylinder_evaluator.md), [EllipticalCone.evaluator](EllipticalCone_evaluator.md), [EllipticalCylinder.evaluator](EllipticalCylinder_evaluator.md), [NurbsSurface.evaluator](NurbsSurface_evaluator.md), [Plane.evaluator](Plane_evaluator.md), [Sphere.evaluator](Sphere_evaluator.md), [Surface.evaluator](Surface_evaluator.md), [Torus.evaluator](Torus_evaluator.md)

## Version

Introduced in version August 2014  

