# Plane Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient plane. A transient plane is not displayed or saved in a document. Transient planes are used as a wrapper to work with raw plane information. A transient plane has no boundaries or size, but is infinite and is represented by a position, a normal, and an orientation in space. They are created statically using the create method of the Plane class.

## Methods

| Name | Description |
|----|----|
| [classType](Plane_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](Plane_copy.md) | Creates and returns an independent copy of this Plane object. |
| [create](Plane_create.md) | Creates a transient plane object by specifying an origin and a normal direction. |
| [createUsingDirections](Plane_createUsingDirections.md) | Creates a transient plane object by specifying an origin along with U and V directions. |
| [intersectWithCurve](Plane_intersectWithCurve.md) | Intersect this plane with a curve to get the intersection point(s). |
| [intersectWithLine](Plane_intersectWithLine.md) | Creates a 3D point at the intersection of this plane and a line. |
| [intersectWithPlane](Plane_intersectWithPlane.md) | Creates an infinite line at the intersection of this plane with another plane. |
| [intersectWithSurface](Plane_intersectWithSurface.md) | Intersect this plane with a surface to get the intersection point(s). |
| [isCoPlanarTo](Plane_isCoPlanarTo.md) | Checks if this plane is coplanar with another plane. |
| [isParallelToLine](Plane_isParallelToLine.md) | Checks if this plane is parallel to a line. |
| [isParallelToPlane](Plane_isParallelToPlane.md) | Checks if this plane is parallel to another plane. |
| [isPerpendicularToLine](Plane_isPerpendicularToLine.md) | Checks if this plane is perpendicular to a line. |
| [isPerpendicularToPlane](Plane_isPerpendicularToPlane.md) | Checks if this plane is perpendicular to another plane. |
| [setUVDirections](Plane_setUVDirections.md) | Sets the U and V directions of the plane. |
| [transformBy](Plane_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [evaluator](Plane_evaluator.md) | Returns the surface evaluator. |
| [isValid](Plane_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [normal](Plane_normal.md) | Gets and sets the normal of the plane. |
| [objectType](Plane_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [origin](Plane_origin.md) | Gets and sets the origin point of the plane. |
| [surfaceType](Plane_surfaceType.md) | Returns the surface type. |
| [uDirection](Plane_uDirection.md) | Gets the U Direction of the plane. |
| [vDirection](Plane_vDirection.md) | Gets the V Direction of the plane. |

## Accessed From

[Canvas.plane](Canvas_plane.md), [CanvasInput.plane](CanvasInput_plane.md), [ConstructionPlane.geometry](ConstructionPlane_geometry.md), [ConstructionPlaneByPlaneDefinition.plane](ConstructionPlaneByPlaneDefinition_plane.md), [OffsetStartDefinition.profilePlane](OffsetStartDefinition_profilePlane.md), [Plane.copy](Plane_copy.md), [Plane.create](Plane_create.md), [Plane.createUsingDirections](Plane_createUsingDirections.md), [Profile.plane](Profile_plane.md), [ProfilePlaneStartDefinition.profilePlane](ProfilePlaneStartDefinition_profilePlane.md)

## Version

Introduced in version August 2014  

