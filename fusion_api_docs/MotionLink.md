# MotionLink Object

Derived from: [Base](Base.md) Object  

## Description

A MotionLink in a design.

## Methods

| Name | Description |
|----|----|
| [classType](MotionLink_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](MotionLink_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](MotionLink_deleteMe.md) | Deletes this MotionLink. |
| [setMotionData](MotionLink_setMotionData.md) | Method that sets the motion data. |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](MotionLink_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](MotionLink_attributes.md) | Returns the collection of attributes associated with this MotionLink. |
| [entityToken](MotionLink_entityToken.md) | Returns a token for the MotionLink object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same MotionLink. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](MotionLink_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [healthState](MotionLink_healthState.md) | Returns the current health state of the MotionLink. |
| [isReversed](MotionLink_isReversed.md) | Gets and sets whether the motion is reversed or not. |
| [isSuppressed](MotionLink_isSuppressed.md) | Gets and sets if this MotionLink is suppressed. |
| [isValid](MotionLink_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointOne](MotionLink_jointOne.md) | Gets the first joint for this MotionLink. |
| [jointTwo](MotionLink_jointTwo.md) | Gets the second joint for this MotionLink. This can return null if the linked motions are from the same joint. |
| [motionOne](MotionLink_motionOne.md) | Gets the first motion type. |
| [motionTwo](MotionLink_motionTwo.md) | Gets the second motion type. |
| [name](MotionLink_name.md) | Gets and sets the name of the MotionLink. |
| [nativeObject](MotionLink_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](MotionLink_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentComponent](MotionLink_parentComponent.md) | Returns the parent component that owns this MotionLink. |
| [timelineObject](MotionLink_timelineObject.md) | Returns the timeline object associated with this MotionLink. |
| [valueOne](MotionLink_valueOne.md) | Returns the ModelParameter for the first motion link value. |
| [valueTwo](MotionLink_valueTwo.md) | Returns the ModelParameter for the second motion link value. |

## Accessed From

[AsBuiltJoint.motionLinks](AsBuiltJoint_motionLinks.md), [Joint.motionLinks](Joint_motionLinks.md), [MotionLink.createForAssemblyContext](MotionLink_createForAssemblyContext.md), [MotionLink.nativeObject](MotionLink_nativeObject.md), [MotionLinks.add](MotionLinks_add.md), [MotionLinks.item](MotionLinks_item.md), [MotionLinks.itemByName](MotionLinks_itemByName.md)

## Version

Introduced in version November 2025  

