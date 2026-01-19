# GeometricConstraintList Object

Derived from: [Base](Base.md) Object  

## Description

A list of geometric constraints.

## Methods

| Name | Description |
|----|----|
| [classType](GeometricConstraintList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](GeometricConstraintList_item.md) | Function that returns the specified geometry constraint using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](GeometricConstraintList_count.md) | Returns the number of constraints in the sketch. |
| [isValid](GeometricConstraintList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](GeometricConstraintList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchArc.geometricConstraints](SketchArc_geometricConstraints.md), [SketchCircle.geometricConstraints](SketchCircle_geometricConstraints.md), [SketchConicCurve.geometricConstraints](SketchConicCurve_geometricConstraints.md), [SketchControlPointSpline.geometricConstraints](SketchControlPointSpline_geometricConstraints.md), [SketchCurve.geometricConstraints](SketchCurve_geometricConstraints.md), [SketchEllipse.geometricConstraints](SketchEllipse_geometricConstraints.md), [SketchEllipticalArc.geometricConstraints](SketchEllipticalArc_geometricConstraints.md), [SketchEntity.geometricConstraints](SketchEntity_geometricConstraints.md), [SketchFittedSpline.geometricConstraints](SketchFittedSpline_geometricConstraints.md), [SketchFixedSpline.geometricConstraints](SketchFixedSpline_geometricConstraints.md), [SketchLine.geometricConstraints](SketchLine_geometricConstraints.md), [SketchPoint.geometricConstraints](SketchPoint_geometricConstraints.md), [SketchText.geometricConstraints](SketchText_geometricConstraints.md)

## Version

Introduced in version August 2014  

