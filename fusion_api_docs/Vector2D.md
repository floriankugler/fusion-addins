# Vector2D Object

Derived from: [Base](Base.md) Object  

## Description

Transient 2D vector. This object is a wrapper for 2D vector data and is used to pass vector data in and out of the API. They are created statically using the create method of the Vector2D class.

## Methods

| Name | Description |
|----|----|
| [add](Vector2D_add.md) | Add a vector to this vector. |
| [angleTo](Vector2D_angleTo.md) | Gets the angle between this vector and another vector. |
| [asArray](Vector2D_asArray.md) | Returns the vector values as an array \[x, y\]. |
| [asPoint](Vector2D_asPoint.md) | Return a point with the same x and y values as this vector. |
| [classType](Vector2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Vector2D_copy.md) | Creates and returns an independent copy of this Vector2D object. |
| [create](Vector2D_create.md) | Creates a 2D vector object. |
| [dotProduct](Vector2D_dotProduct.md) | Calculates the Dot Product of this vector and an input vector. |
| [isEqualTo](Vector2D_isEqualTo.md) | Compare this vector with another to check for equality. |
| [isParallelTo](Vector2D_isParallelTo.md) | Compare this vector with another to check for parallelism. |
| [isPerpendicularTo](Vector2D_isPerpendicularTo.md) | Compare this vector with another to check for perpendicularity. |
| [normalize](Vector2D_normalize.md) | Normalizes the vector. Normalization makes the vector length equal to one. The vector should not be zero length. |
| [scaleBy](Vector2D_scaleBy.md) | Scales the vector by specifying a scaling factor. |
| [setWithArray](Vector2D_setWithArray.md) | Sets the definition of the vector by specifying an array containing the x and y coordinates. |
| [subtract](Vector2D_subtract.md) | Subtract a vector from this vector. |
| [transformBy](Vector2D_transformBy.md) | Transforms the vector by specifying a 2D transformation matrix. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](Vector2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [length](Vector2D_length.md) | Gets the length of the vector. |
| [objectType](Vector2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [x](Vector2D_x.md) | Gets and sets the X coordinate of the vector. |
| [y](Vector2D_y.md) | Gets and sets the Y coordinate of the vector. |

## Accessed From

[CurveEvaluator2D.getCurvature](CurveEvaluator2D_getCurvature.md), [CurveEvaluator2D.getFirstDerivative](CurveEvaluator2D_getFirstDerivative.md), [CurveEvaluator2D.getSecondDerivative](CurveEvaluator2D_getSecondDerivative.md), [CurveEvaluator2D.getTangent](CurveEvaluator2D_getTangent.md), [CurveEvaluator2D.getThirdDerivative](CurveEvaluator2D_getThirdDerivative.md), [Ellipse2D.getData](Ellipse2D_getData.md), [Ellipse2D.majorAxis](Ellipse2D_majorAxis.md), [EllipticalArc2D.getData](EllipticalArc2D_getData.md), [EllipticalArc2D.majorAxis](EllipticalArc2D_majorAxis.md), [Matrix2D.getAsCoordinateSystem](Matrix2D_getAsCoordinateSystem.md), [Point2D.asVector](Point2D_asVector.md), [Point2D.vectorTo](Point2D_vectorTo.md), [Vector2D.copy](Vector2D_copy.md), [Vector2D.create](Vector2D_create.md)

## Version

Introduced in version August 2014  

