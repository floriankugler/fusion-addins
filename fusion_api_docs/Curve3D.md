# Curve3D Object

Derived from: [Base](Base.md) Object  

## Description

The base class for all 3D transient geometry classes.

## Methods

| Name | Description |
|----|----|
| [classType](Curve3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [transformBy](Curve3D_transformBy.md) | Transforms this curve in 3D space. |

## Properties

| Name | Description |
| --- | --- |
| [curveType](Curve3D_curveType.md) | Returns the type of geometry this curve represents. |
| [evaluator](Curve3D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](Curve3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Curve3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[BRepEdge.geometry](BRepEdge_geometry.md), [BRepEdgeDefinition.modelSpaceCurve](BRepEdgeDefinition_modelSpaceCurve.md), [BRepWireEdgeDefinition.modelSpaceCurve](BRepWireEdgeDefinition_modelSpaceCurve.md), [Curve3DPath.item](Curve3DPath_item.md), [CustomGraphicsCurve.curve](CustomGraphicsCurve_curve.md), [PathEntity.curve](PathEntity_curve.md), [ProfileCurve.geometry](ProfileCurve_geometry.md), [SketchText.asCurves](SketchText_asCurves.md)

## Derived Classes

[Arc3D](Arc3D.md), [Circle3D](Circle3D.md), [Ellipse3D](Ellipse3D.md), [EllipticalArc3D](EllipticalArc3D.md), [InfiniteLine3D](InfiniteLine3D.md), [Line3D](Line3D.md), [NurbsCurve3D](NurbsCurve3D.md), [Polyline3D](Polyline3D.md)

## Version

Introduced in version August 2014  

