# PolygonConstraint Object

Derived from: [GeometricConstraint](GeometricConstraint.md) Object  

## Description

A polygon constraint in a sketch.

## Methods

| Name | Description |
|----|----|
| [classType](PolygonConstraint_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](PolygonConstraint_deleteMe.md) | Deletes this constraint. The IsDeletable property can be used to determine if this constraint can be deleted. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](PolygonConstraint_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](PolygonConstraint_attributes.md) | Returns the collection of attributes associated with this geometric constraint. |
| [centerPoint](PolygonConstraint_centerPoint.md) | Returns the SketchPoint that acts as the center point of the polygon. |
| [entityToken](PolygonConstraint_entityToken.md) | Returns a token for the GeometricConstraint object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same geometric constraint. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [isDeletable](PolygonConstraint_isDeletable.md) | Indicates if this constraint is deletable. |
| [isValid](PolygonConstraint_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [lines](PolygonConstraint_lines.md) | **RETIRED** This has been retired and you should use the points property instead. |
| [objectType](PolygonConstraint_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentSketch](PolygonConstraint_parentSketch.md) | Returns the parent sketch object. |
| [points](PolygonConstraint_points.md) | Returns the sketch points that define the vertices of the polygon. The sketch lines that draw the shape of the polygon can be obtained from the points. |

## Accessed From

[GeometricConstraints.addPolygon](GeometricConstraints_addPolygon.md)

## Version

Introduced in version March 2016  

