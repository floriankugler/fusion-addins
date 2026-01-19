# GeometricConstraints Object

Derived from: [Base](Base.md) Object  

## Description

A collection of all of the geometric constraints in a sketch. This object also supports the methods to create new geometric constraints.

## Methods

| Name | Description |
| --- | --- |
| [addCircularPattern](GeometricConstraints_addCircularPattern.md) | Creates a new circular pattern in the sketch. |
| [addCoincident](GeometricConstraints_addCoincident.md) | Creates a new coincident constraint between two entities. The first argument is a sketch point. The second argument is a sketch curve or point. |
| [addCoincidentToSurface](GeometricConstraints_addCoincidentToSurface.md) | Creates a new coincident constraint between the sketch point and surface. This forces the point to lie on the surface. |
| [addCollinear](GeometricConstraints_addCollinear.md) | Creates a new collinear constraint between two lines. |
| [addConcentric](GeometricConstraints_addConcentric.md) | Creates a new concentric constraint between two circles, arcs, ellipses, or elliptical arcs. |
| [addEqual](GeometricConstraints_addEqual.md) | Creates a new equal constraint between two lines, or between arcs and circles. |
| [addHorizontal](GeometricConstraints_addHorizontal.md) | Creates a new horizontal constraint on a line. |
| [addHorizontalPoints](GeometricConstraints_addHorizontalPoints.md) | Creates a new horizontal constraint between two points. |
| [addLineOnPlanarSurface](GeometricConstraints_addLineOnPlanarSurface.md) | Creates a new constraint that forces the sketch line to lie on a planar surface. |
| [addLineParallelToPlanarSurface](GeometricConstraints_addLineParallelToPlanarSurface.md) | Creates a new parallel constraint between a sketch line and a planar surface that will constrain the line to lie on a plane parallel to the specified surface. |
| [addMidPoint](GeometricConstraints_addMidPoint.md) | Creates a new midpoint constraint between a point and a curve. |
| [addOffset](GeometricConstraints_addOffset.md) | **RETIRED** Creates an offset constraint, which results in creating a new set of curves that are an offset of the input curves. The returned offset constraint provides access to the created curves and the parameter controlling the offset. The offset direction is implied by the flow direction of the provided curves. For example, if two connected lines are offset, the flow direction is from line 1 to line 2. A positive offset value creates the offset curve to the "right" of the lines and a negative offset goes to the "left". Left and right are evaluated with respect to the geometry. If you are standing on line 1 looking towards line 2 your left and right are the offset left and right. For closed single curves like circles and ellipses their flow direction is always counterclockwise so a positive offset is always to the outsides. |
| [addOffset2](GeometricConstraints_addOffset2.md) | Creates an offset constraint, which results in creating a new set of curves that are an offset of the input curves. The returned offset constraint object provides access to the created curves and the parameter controlling the offset. |
| [addParallel](GeometricConstraints_addParallel.md) | Creates a new parallel constraint between two lines. |
| [addPerpendicular](GeometricConstraints_addPerpendicular.md) | Creates a new perpendicular constraint between two lines. |
| [addPerpendicularToSurface](GeometricConstraints_addPerpendicularToSurface.md) | Creates a new perpendicular constraint that forces the sketch curve to be perpendicular to the specified surface. Line and spline curves are supported. |
| [addPolygon](GeometricConstraints_addPolygon.md) | Creates a polygon constraint on existing lines in the sketch. |
| [addRectangularPattern](GeometricConstraints_addRectangularPattern.md) | Creates a new rectangular pattern in the sketch. |
| [addSmooth](GeometricConstraints_addSmooth.md) | Creates a new smooth constraint between two curves. One of the curves must be a spline. The other curve can be a spline or any other type of curve. |
| [addSymmetry](GeometricConstraints_addSymmetry.md) | Creates a new symmetry constraint. |
| [addTangent](GeometricConstraints_addTangent.md) | Creates a new tangent constraint between two curves. |
| [addTwoSidesOffset](GeometricConstraints_addTwoSidesOffset.md) | Creates two offset constraints, which results in creating two new sets of curves that are an offset of the input curves on each side of the original set of curves. The returned offset constraint objects provide access to the created curves and the parameters controlling the offsets. |
| [addVertical](GeometricConstraints_addVertical.md) | Creates a new vertical constraint on a line. |
| [addVerticalPoints](GeometricConstraints_addVerticalPoints.md) | Creates a new vertical constraint between two points. |
| [classType](GeometricConstraints_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createCircularPatternInput](GeometricConstraints_createCircularPatternInput.md) | Creates a CircularPatternConstraintInput object. Use properties and methods on this object to define the circular pattern you want to create and then use the Add method, passing in the CircularPatternConstraintInput object. |
| [createOffsetInput](GeometricConstraints_createOffsetInput.md) | Creates an OffsetConstraintInput object. Use properties and methods on this object to define the offset you want to create and then use the addOffset2 method, passing in the OffsetConstraintInput object, to create the offset. |
| [createRectangularPatternInput](GeometricConstraints_createRectangularPatternInput.md) | Creates a new RectangularPatternConstraintInput object. Use this object to define the various settings associated with a rectangular pattern in a sketch. Once the pattern is defined you can call the addRectangularPattern method and pass in the input object to create the sketch rectangular pattern. |
| [item](GeometricConstraints_item.md) | Function that returns the specified sketch constraint using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](GeometricConstraints_count.md) | Returns the number of constraints in the sketch. |
| [isValid](GeometricConstraints_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](GeometricConstraints_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Sketch.geometricConstraints](Sketch_geometricConstraints.md)

## Samples

| Name | Description |
|----|----|
| [API Sample that demonstrates creating sketch lines in various ways.](CreateSketchLines_Sample.md) | Demonstrates several ways to create sketch lines, including as the result of creating a rectangle. |
| [GeometricConstraints.addConcentric](GeometricConstraints_addConcentric_Sample.md) | Demonstrates the GeometricConstraints.addConcentric method. |

## Version

Introduced in version August 2014  

