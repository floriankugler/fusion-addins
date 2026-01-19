# OffsetConstraint Object

Derived from: [GeometricConstraint](GeometricConstraint.md) Object  

## Description

An offset constraint in a sketch.

## Methods

| Name | Description |
|----|----|
| [classType](OffsetConstraint_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](OffsetConstraint_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](OffsetConstraint_deleteMe.md) | Deletes this constraint. The IsDeletable property can be used to determine if this constraint can be deleted. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](OffsetConstraint_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](OffsetConstraint_attributes.md) | Returns the collection of attributes associated with this geometric constraint. |
| [childCurves](OffsetConstraint_childCurves.md) | Returns an array of sketch curves that are the set of child curves resulting from the offset. Nothing should be assumed about the order in how the curves are returned. |
| [dimension](OffsetConstraint_dimension.md) | Returns the dimension controlling the offset distance. This can return null in the case where the dimension has been deleted. To change the offset distance you can use the parameter property of the returned dimension to get the parameter that controls the value and use properties on the parameter to change the value. This can return either a SketchOffsetCurvesDimension or a SketchOffsetDimension. A SketchOffsetCurvesDimension is created automatically when curves are offset but if it is deleted the offset can also be controlled by a SketchOffsetDimension. |
| [distance](OffsetConstraint_distance.md) | The current distance of the offset in centimeters. To change the offset you need to modify the value of the parameter associated with the dimension, which you can get using the dimension property. |
| [entityToken](OffsetConstraint_entityToken.md) | Returns a token for the GeometricConstraint object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same geometric constraint. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [isDeletable](OffsetConstraint_isDeletable.md) | Indicates if this constraint is deletable. |
| [isTopologyMatched](OffsetConstraint_isTopologyMatched.md) | Gets the setting that controls if the offset curves match the topology of the original curves. |
| [isValid](OffsetConstraint_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [nativeObject](OffsetConstraint_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](OffsetConstraint_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentCurves](OffsetConstraint_parentCurves.md) | Returns an array of sketch curves that are the set of parent curves. Nothing should be assumed about the order in how the curves are returned. |
| [parentSketch](OffsetConstraint_parentSketch.md) | Returns the parent sketch object. |

## Accessed From

[GeometricConstraints.addOffset](GeometricConstraints_addOffset.md), [GeometricConstraints.addOffset2](GeometricConstraints_addOffset2.md), [GeometricConstraints.addTwoSidesOffset](GeometricConstraints_addTwoSidesOffset.md), [OffsetConstraint.createForAssemblyContext](OffsetConstraint_createForAssemblyContext.md), [OffsetConstraint.nativeObject](OffsetConstraint_nativeObject.md), [SketchOffsetCurvesDimension.offsetConstraint](SketchOffsetCurvesDimension_offsetConstraint.md)

## Version

Introduced in version March 2016  

