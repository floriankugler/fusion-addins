# SketchDimensionList Object

Derived from: [Base](Base.md) Object  

## Description

A list of sketch dimensions.

## Methods

| Name | Description |
|----|----|
| [classType](SketchDimensionList_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchDimensionList_item.md) | Function that returns the specified sketch dimension using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchDimensionList_count.md) | Returns the number of sketch dimensions in the sketch. |
| [isValid](SketchDimensionList_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchDimensionList_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[SketchArc.sketchDimensions](SketchArc_sketchDimensions.md), [SketchCircle.sketchDimensions](SketchCircle_sketchDimensions.md), [SketchConicCurve.sketchDimensions](SketchConicCurve_sketchDimensions.md), [SketchControlPointSpline.sketchDimensions](SketchControlPointSpline_sketchDimensions.md), [SketchCurve.sketchDimensions](SketchCurve_sketchDimensions.md), [SketchEllipse.sketchDimensions](SketchEllipse_sketchDimensions.md), [SketchEllipticalArc.sketchDimensions](SketchEllipticalArc_sketchDimensions.md), [SketchEntity.sketchDimensions](SketchEntity_sketchDimensions.md), [SketchFittedSpline.sketchDimensions](SketchFittedSpline_sketchDimensions.md), [SketchFixedSpline.sketchDimensions](SketchFixedSpline_sketchDimensions.md), [SketchLine.sketchDimensions](SketchLine_sketchDimensions.md), [SketchPoint.sketchDimensions](SketchPoint_sketchDimensions.md), [SketchText.sketchDimensions](SketchText_sketchDimensions.md)

## Version

Introduced in version August 2014  

