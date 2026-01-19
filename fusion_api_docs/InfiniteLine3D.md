# InfiniteLine3D Object

Derived from: [Curve3D](Curve3D.md) Object  

## Description

Transient 3D infinite line. An infinite line is defined by a position and direction in space and has no start or end points. They are created statically using the create method of the InfiniteLine3D class.

## Methods

| Name | Description |
|----|----|
| [classType](InfiniteLine3D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](InfiniteLine3D_copy.md) | Creates and returns a copy of this line object. |
| [create](InfiniteLine3D_create.md) | Creates a transient 3D infinite line. |
| [getData](InfiniteLine3D_getData.md) | Gets all of the data defining the infinite line. |
| [intersectWithCurve](InfiniteLine3D_intersectWithCurve.md) | Intersect this line with a curve to get the intersection point(s). |
| [intersectWithSurface](InfiniteLine3D_intersectWithSurface.md) | Intersect this line with a surface to get the intersection point(s). |
| [isColinearTo](InfiniteLine3D_isColinearTo.md) | Compare this line with another to check for collinearity. |
| [set](InfiniteLine3D_set.md) | Sets all of the data defining the infinite line. |
| [transformBy](InfiniteLine3D_transformBy.md) | Transforms this curve in 3D space. |

## Properties

| Name | Description |
| --- | --- |
| [curveType](InfiniteLine3D_curveType.md) | Returns the type of geometry this curve represents. |
| [direction](InfiniteLine3D_direction.md) | Gets and sets the direction of the line. |
| [evaluator](InfiniteLine3D_evaluator.md) | Returns an evaluator object that lets you perform additional evaluations on the curve. |
| [isValid](InfiniteLine3D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](InfiniteLine3D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](InfiniteLine3D_origin.md) | Gets and sets the origin point of the line. |

## Accessed From

[ConstructionAxis.geometry](ConstructionAxis_geometry.md), [ConstructionAxisByLineDefinition.axis](ConstructionAxisByLineDefinition_axis.md), [InfiniteLine3D.copy](InfiniteLine3D_copy.md), [InfiniteLine3D.create](InfiniteLine3D_create.md), [Line3D.asInfiniteLine](Line3D_asInfiniteLine.md), [Plane.intersectWithPlane](Plane_intersectWithPlane.md), [RotaryMachineAxis.rotationAxis](RotaryMachineAxis_rotationAxis.md), [RotaryMachineAxisInput.rotationAxis](RotaryMachineAxisInput_rotationAxis.md)

## Version

Introduced in version August 2014  

