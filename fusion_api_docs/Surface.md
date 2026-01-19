# Surface Object

Derived from: [Base](Base.md) Object  

## Description

Describes a two-dimensional topological, manifold in three-dimensional space. It is used as the underlying geometry for a BRepFace.

## Methods

| Name | Description |
|----|----|
| [classType](Surface_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [transformBy](Surface_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [evaluator](Surface_evaluator.md) | Returns the surface evaluator. |
| [isValid](Surface_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Surface_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [surfaceType](Surface_surfaceType.md) | Returns the surface type. |

## Accessed From

[BRepFace.geometry](BRepFace_geometry.md), [BRepFaceDefinition.surfaceGeometry](BRepFaceDefinition_surfaceGeometry.md)

## Derived Classes

[Cone](Cone.md), [Cylinder](Cylinder.md), [EllipticalCone](EllipticalCone.md), [EllipticalCylinder](EllipticalCylinder.md), [NurbsSurface](NurbsSurface.md), [Plane](Plane.md), [Sphere](Sphere.md), [Torus](Torus.md)

## Version

Introduced in version August 2014  

