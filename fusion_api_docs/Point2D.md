# Point2D Object

Derived from: [Base](Base.md) Object  

## Description

Transient 2D point. A transient point is not displayed or saved in a document. Transient 2D points are used as a wrapper to work with raw 2D point information. They are created statically using the create methods of the Point2D class.

## Methods

| Name | Description |
|----|----|
| [asArray](Point2D_asArray.md) | Get coordinate data of the point |
| [asVector](Point2D_asVector.md) | Defines a vector using the coordinates of the point. |
| [classType](Point2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Point2D_copy.md) | Creates and returns a copy of this point object. |
| [create](Point2D_create.md) | Creates a transient 2D point object. |
| [distanceTo](Point2D_distanceTo.md) | Returns the distance from this point to another point. |
| [getData](Point2D_getData.md) | Gets the data defining the point. |
| [isEqualTo](Point2D_isEqualTo.md) | Checks to see if this point and another point are equal (have identical coordinates). The comparison is done within the modeling tolerance which can be found with the Application.pointTolerance property. If you want to compare two points with any other tolerance you can use the isEqualToByTolerance method. |
| [isEqualToByTolerance](Point2D_isEqualToByTolerance.md) | Checks to see if this point and another point are equal within the specified tolerance. |
| [set](Point2D_set.md) | Sets the coordinates of the point by specifying the x, y coordinates. |
| [setWithArray](Point2D_setWithArray.md) | Sets the coordinates of the point using an array as input. |
| [transformBy](Point2D_transformBy.md) | Transforms the point using the provided matrix. |
| [translateBy](Point2D_translateBy.md) | Translates the point using the provided vector. |
| [vectorTo](Point2D_vectorTo.md) | Returns a vector from this point to another point. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Point2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Point2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [x](Point2D_x.md) | Gets and sets the X coordinate of the point. |
| [y](Point2D_y.md) | Gets and sets the Y coordinate of the point. |

## Accessed From

[Arc2D.center](Arc2D_center.md), [Arc2D.endPoint](Arc2D_endPoint.md), [Arc2D.getData](Arc2D_getData.md), [Arc2D.startPoint](Arc2D_startPoint.md), [BoundingBox2D.maxPoint](BoundingBox2D_maxPoint.md), [BoundingBox2D.minPoint](BoundingBox2D_minPoint.md), [Circle2D.center](Circle2D_center.md), [Circle2D.getData](Circle2D_getData.md), [CurveEvaluator2D.getEndPoints](CurveEvaluator2D_getEndPoints.md), [CurveEvaluator2D.getPointAtParameter](CurveEvaluator2D_getPointAtParameter.md), [CustomGraphicsViewPlacement.viewPoint](CustomGraphicsViewPlacement_viewPoint.md), [DXF2DImportOptions.position](DXF2DImportOptions_position.md), [Ellipse2D.center](Ellipse2D_center.md), [Ellipse2D.getData](Ellipse2D_getData.md), [EllipticalArc2D.center](EllipticalArc2D_center.md), [EllipticalArc2D.endPoint](EllipticalArc2D_endPoint.md), [EllipticalArc2D.getData](EllipticalArc2D_getData.md), [EllipticalArc2D.startPoint](EllipticalArc2D_startPoint.md), [Line2D.endPoint](Line2D_endPoint.md), [Line2D.getData](Line2D_getData.md), [Line2D.startPoint](Line2D_startPoint.md), [Matrix2D.getAsCoordinateSystem](Matrix2D_getAsCoordinateSystem.md), [MouseEventArgs.position](MouseEventArgs_position.md), [MouseEventArgs.viewportPosition](MouseEventArgs_viewportPosition.md), [NurbsCurve2D.controlPoints](NurbsCurve2D_controlPoints.md), [Point2D.copy](Point2D_copy.md), [Point2D.create](Point2D_create.md), [Polyline2D.points](Polyline2D_points.md), [SurfaceEvaluator.getParameterAtPoint](SurfaceEvaluator_getParameterAtPoint.md), [TriangleMesh.textureCoordinates](TriangleMesh_textureCoordinates.md), [Vector2D.asPoint](Vector2D_asPoint.md), [Viewport.modelToViewSpace](Viewport_modelToViewSpace.md), [Viewport.screenToView](Viewport_screenToView.md), [Viewport.viewToScreen](Viewport_viewToScreen.md)

## Version

Introduced in version August 2014  

