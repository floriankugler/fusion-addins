# BoundingBox2D Object

Derived from: [Base](Base.md) Object  

## Description

Transient object that represents a 2D bounding box. A 2D bounding box is a rectangle box that is parallel to the x and y axes. The box is defined by a minimum point (smallest x-y values) and maximum point (largest x-y values). This object is a wrapper for these points and serves as a way to pass bounding box information in and out of functions. It also provides some convenience function when working with the bounding box data. They are created statically using the create method of the BoundingBox2D class.

## Methods

| Name | Description |
|----|----|
| [classType](BoundingBox2D_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [combine](BoundingBox2D_combine.md) | Combines this bounding box with the input bounding box. If the input bounding box extends outside this bounding box then this bounding box will be extended to encompass both of the original bounding boxes. |
| [contains](BoundingBox2D_contains.md) | Determines if the specified point lies within the bounding box. |
| [copy](BoundingBox2D_copy.md) | Create a copy of this bounding box. |
| [create](BoundingBox2D_create.md) | Creates a transient bounding box object. |
| [expand](BoundingBox2D_expand.md) | Expand this bounding box to contain the specified point. |
| [intersects](BoundingBox2D_intersects.md) | Test if this bounding box intersects with the specified bounding box. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](BoundingBox2D_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [maxPoint](BoundingBox2D_maxPoint.md) | Gets and sets the maximum point of the box. |
| [minPoint](BoundingBox2D_minPoint.md) | Gets and sets the minimum point of the box. |
| [objectType](BoundingBox2D_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[ArrangePlaneResultEnvelope.boundingBox](ArrangePlaneResultEnvelope_boundingBox.md), [BoundingBox2D.copy](BoundingBox2D_copy.md), [BoundingBox2D.create](BoundingBox2D_create.md), [ConstructionPlane.displayBounds](ConstructionPlane_displayBounds.md), [SurfaceEvaluator.parametricRange](SurfaceEvaluator_parametricRange.md)

## Version

Introduced in version August 2014  

