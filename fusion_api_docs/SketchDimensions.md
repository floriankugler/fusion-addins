# SketchDimensions Object

Derived from: [Base](Base.md) Object  

## Description

A collection of the dimensions in a sketch. This object also supports the methods to add new sketch dimensions.

## Methods

| Name | Description |
|----|----|
| [addAngularDimension](SketchDimensions_addAngularDimension.md) | Creates a new angular dimension constraint between the two input lines. The position of the text controls which of the four quadrants will be dimensioned. |
| [addConcentricCircleDimension](SketchDimensions_addConcentricCircleDimension.md) | Creates a new dimension constraint between to concentric circles or arcs. |
| [addDiameterDimension](SketchDimensions_addDiameterDimension.md) | Creates a new diameter dimension constraint on the arc or circle. |
| [addDistanceBetweenLineAndPlanarSurfaceDimension](SketchDimensions_addDistanceBetweenLineAndPlanarSurfaceDimension.md) | Creates a new linear dimension controlling the distance between a sketch line and the specified planar face or construction plane. The sketch line must lie on a plane that is parallel to the planar surface. The text position is automatically chosen and is positioned so it is midway between the line and surface and the extension lines are a minimum length. You can modify the position by using functionality on the returned SketchDistanceBetweenLineAndPlanarSurfaceDimension object. |
| [addDistanceBetweenPointAndSurfaceDimension](SketchDimensions_addDistanceBetweenPointAndSurfaceDimension.md) | Creates a new linear dimension controlling the distance between a sketch point and the specified surface or point. The text position is automatically chosen and is positioned so it is midway between the point and surface and the extension lines are a minimum length. You can modify the position by using functionality on the returned SketchDistanceBetweenPointAndSurfaceDimension object. |
| [addDistanceDimension](SketchDimensions_addDistanceDimension.md) | Creates a new linear dimension constraint between the two input entities. |
| [addEllipseMajorRadiusDimension](SketchDimensions_addEllipseMajorRadiusDimension.md) | Creates a new dimension constraint on the major radius of an ellipse. |
| [addEllipseMinorRadiusDimension](SketchDimensions_addEllipseMinorRadiusDimension.md) | Creates a new dimension constraint on the minor radius of an ellipse. |
| [addLinearDiameterDimension](SketchDimensions_addLinearDiameterDimension.md) | Creates a new linear dimension showing the diameter where the first line acts as the center line and the second entity defines the size. The first input entity must be a sketch line. The second entity can be a point or a line that is parallel to the first. The dimension controls the distance as measured perpendicular to the first input line. |
| [addOffsetDimension](SketchDimensions_addOffsetDimension.md) | Creates a new linear dimension constraint between the two input entities. The first input entity must be a sketch line. The second entity can be a point or a line that is parallel to the first. The dimension controls the distance as measured perpendicular to the first input line. |
| [addRadialDimension](SketchDimensions_addRadialDimension.md) | Creates a new radial dimension constraint on the arc or circle. |
| [addTangentDistanceDimension](SketchDimensions_addTangentDistanceDimension.md) | Creates a new linear dimension from between a line and circle or arc and a second circle or arc where the dimension is to the tangent on the edge of the circle or arc. |
| [classType](SketchDimensions_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](SketchDimensions_item.md) | Function that returns the specified sketch dimension using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](SketchDimensions_count.md) | Returns the number of sketch dimensions in the sketch. |
| [isValid](SketchDimensions_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchDimensions_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Sketch.sketchDimensions](Sketch_sketchDimensions.md)

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [SketchDimensions.addAngularDimension](SketchDimension_addAngularDimension_Sample.md) | Demonstrates the SketchDimension.addAngularDimension method. |
| [SketchDimensions.addConcentricCicleDimension](SketchDimension_addConcentricCircleDimension_Sample.md) | Demonstrates the SketchDimension.addConcentricCircleDimension method. |
| [SketchDimensions.addDiameterDimension](SketchDimension_addDiameterDimension_Sample.md) | Demonstrates the SketchDimension.addDiameterDimension method. |
| [SketchDimensions.addDistanceDimension](SketchDimension_addDistanceDimension_Sample.md) | Demonstrates the SketchDimension.addDistanceDimension method. |
| [SketchDimensions.AddEllipseMajorRadiusDimension](SketchDimension_addEllipseMajorRadiusDimension_Sample.md) | Demonstrates the SketchDimension.addEllipseMajorRadiusDimension method. |
| [SketchDimensions.AddEllipseMinorRadiusDimension](SketchDimension_addEllipseMinorRadiusDimension_Sample.md) | Demonstrates the SketchDimension.addEllipseMinorRadiusDimension method. |
| [SketchDimensions.addOffsetDimension](SketchDimension_addOffsetDimension_Sample.md) | Demonstrates the SketchDimension.addOffsetDimension method. |

## Version

Introduced in version August 2014  

