# SketchLinearDimension Object

Derived from: [SketchDimension](SketchDimension.md) Object  

## Description

A linear dimension in a sketch.

## Methods

| Name | Description |
|----|----|
| [classType](SketchLinearDimension_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](SketchLinearDimension_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](SketchLinearDimension_deleteMe.md) | Deletes this dimension. The IsDeletable property indicates if this dimension can be deleted. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](SketchLinearDimension_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](SketchLinearDimension_attributes.md) | Returns the collection of attributes associated with this sketch dimension. |
| [entityOne](SketchLinearDimension_entityOne.md) | The first entity being constrained. |
| [entityToken](SketchLinearDimension_entityToken.md) | Returns a token for the SketchDimension object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same sketch dimension. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [entityTwo](SketchLinearDimension_entityTwo.md) | The second entity being constrained. |
| [isDeletable](SketchLinearDimension_isDeletable.md) | Indicates if this dimension is deletable. |
| [isDriving](SketchLinearDimension_isDriving.md) | Gets and sets if the dimension is Driving or is Driven. Setting this property to true for a given dimension may fail if the result would over constrain the sketch. Fusion does not allow over-constrained sketches. |
| [isValid](SketchLinearDimension_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [nativeObject](SketchLinearDimension_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](SketchLinearDimension_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [orientation](SketchLinearDimension_orientation.md) | The orientation of this dimension. |
| [parameter](SketchLinearDimension_parameter.md) | Returns the associated parameter or null if there is no associated parameter. |
| [parentSketch](SketchLinearDimension_parentSketch.md) | Returns the parent sketch object. |
| [textPosition](SketchLinearDimension_textPosition.md) | Gets and sets position of the dimension text. |
| [value](SketchLinearDimension_value.md) | Gets and sets the current value of the sketch dimension. In a parametric modeling design and the isDriving property is True, this is exactly equivalent to getting the parameter associated with the dimension and editing its value. Editing this property will result in the parameter value being changed. If isDriving is False, this acts as a read-only property and attempting to set it will fail. In a direct modeling design the parameter property will return null and this property can be used to get and set the value of the dimension because in this case, there isn't an associated parameter. The value is always in internal units which means that for dimensions that represent a distance, the value is in Centimeters and for dimensions representing an angle the value is in Radians. |

## Accessed From

[SketchDimensions.addDistanceDimension](SketchDimensions_addDistanceDimension.md), [SketchLinearDimension.createForAssemblyContext](SketchLinearDimension_createForAssemblyContext.md), [SketchLinearDimension.nativeObject](SketchLinearDimension_nativeObject.md)

## Version

Introduced in version August 2014  

