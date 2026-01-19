# NurbsSurface Object

Derived from: [Surface](Surface.md) Object  

## Description

Transient NURBS surface. A transient NURBS surface is not displayed or saved in a document. A transient NURBS surface is used as a wrapper to work with raw NURBS surface information. A transient NURBS surface is bounded by it's natural boundaries and does not support the definition of arbitrary boundaries. A NURBS surface is typically obtained from a BREPFace object, which does have boundary information. They are created statically using the create method of the NurbsSurface class.

## Methods

| Name | Description |
|----|----|
| [classType](NurbsSurface_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](NurbsSurface_copy.md) | Creates and returns an independent copy of this NurbsSurface object. |
| [create](NurbsSurface_create.md) | Creates a transient NURBS surface object. |
| [getData](NurbsSurface_getData.md) | Gets the data that defines the NURBS surface. |
| [set](NurbsSurface_set.md) | Sets the data that defines the NURBS surface. |
| [transformBy](NurbsSurface_transformBy.md) | Updates this surface by transforming it with a given input matrix. |

## Properties

| Name | Description |
| --- | --- |
| [controlPointCountU](NurbsSurface_controlPointCountU.md) | Gets the number of control points in the U direction. |
| [controlPointCountV](NurbsSurface_controlPointCountV.md) | Gets the number of control points in the V direction. |
| [controlPoints](NurbsSurface_controlPoints.md) | Gets an array of control points from the surface. |
| [degreeU](NurbsSurface_degreeU.md) | Gets the degree in the U direction. |
| [degreeV](NurbsSurface_degreeV.md) | Gets the degree in the V direction. |
| [evaluator](NurbsSurface_evaluator.md) | Returns the surface evaluator. |
| [isValid](NurbsSurface_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [knotCountU](NurbsSurface_knotCountU.md) | Gets the knot count in the U direction. |
| [knotCountV](NurbsSurface_knotCountV.md) | Gets thekKnot count in the V direction. |
| [knotsU](NurbsSurface_knotsU.md) | Get the knot vector from the U direction. |
| [knotsV](NurbsSurface_knotsV.md) | Get the knot vector from the V direction |
| [objectType](NurbsSurface_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [propertiesU](NurbsSurface_propertiesU.md) | Gets the properties (NurbsSurfaceProperties) of the surface in the U direction. |
| [propertiesV](NurbsSurface_propertiesV.md) | Gets the properties (NurbsSurfaceProperties) of the surface in the V direction. |
| [surfaceType](NurbsSurface_surfaceType.md) | Returns the surface type. |

## Accessed From

[NurbsSurface.copy](NurbsSurface_copy.md), [NurbsSurface.create](NurbsSurface_create.md)

## Version

Introduced in version August 2014  

