# AsBuiltJoint Object

Derived from: [Base](Base.md) Object  

## Description

Represent an as-built joint.

## Methods

| Name | Description |
| --- | --- |
| [classType](AsBuiltJoint_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](AsBuiltJoint_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](AsBuiltJoint_deleteMe.md) | Deletes this as-built joint. |
| [setAsBallJointMotion](AsBuiltJoint_setAsBallJointMotion.md) | Redefines the relationship between the two joint geometries as a ball joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [setAsCylindricalJointMotion](AsBuiltJoint_setAsCylindricalJointMotion.md) | Redefines the relationship between the two joint geometries as a cylindrical joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [setAsPinSlotJointMotion](AsBuiltJoint_setAsPinSlotJointMotion.md) | Redefines the relationship between the two joint geometries as a pin-slot joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [setAsPlanarJointMotion](AsBuiltJoint_setAsPlanarJointMotion.md) | Redefines the relationship between the two joint geometries as a planar joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [setAsRevoluteJointMotion](AsBuiltJoint_setAsRevoluteJointMotion.md) | Redefines the relationship between the two joint geometries as a revolute joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [setAsRigidJointMotion](AsBuiltJoint_setAsRigidJointMotion.md) | Redefines the relationship between the two joint geometries as a rigid joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [setAsSliderJointMotion](AsBuiltJoint_setAsSliderJointMotion.md) | Redefines the relationship between the two joint geometries as a slider joint. To use this method, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [assemblyContext](AsBuiltJoint_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](AsBuiltJoint_attributes.md) | Returns the collection of attributes associated with this as-built joint. |
| [entityToken](AsBuiltJoint_entityToken.md) | Returns a token for the AsBuiltJoint object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same as-built joint. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [geometry](AsBuiltJoint_geometry.md) | Specifies the position of the joint. Getting this property will return null and setting it will be ignored in the case where the joint motion is rigid. To set this property, you need to position the timeline marker to immediately before this as-built joint. This can be accomplished using the following code: thisAsBuiltJoint.timelineObject.rollTo(True) |
| [isLightBulbOn](AsBuiltJoint_isLightBulbOn.md) | Gets and sets if the light bulb of this as-built joint as displayed in the browser is on or off. A joint will only be visible if the light bulb is switched on. However, the light bulb can be on and the joint still invisible if a higher level occurrence in the assembly context is not visible because its light bulb is off or the joints folder is light bulb is off. |
| [isSuppressed](AsBuiltJoint_isSuppressed.md) | Gets and sets if this as-built joint is suppressed. |
| [isValid](AsBuiltJoint_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](AsBuiltJoint_isVisible.md) | Gets whether the as-built joint is visible. To change the visibility see the isLightBulbOn property. This property is affected by the assembly context. |
| [jointMotion](AsBuiltJoint_jointMotion.md) | Returns a JointMotion object that defines the motion relationship between the two geometries. |
| [motionLinks](AsBuiltJoint_motionLinks.md) | Returns the MotionLink objects that this joint is involved in. |
| [name](AsBuiltJoint_name.md) | The name of the as-built joint as it is displayed in the timeline and the browser. The name can be changed. |
| [nativeObject](AsBuiltJoint_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](AsBuiltJoint_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrenceOne](AsBuiltJoint_occurrenceOne.md) | Specifies the first of two occurrences the joint is between. |
| [occurrenceTwo](AsBuiltJoint_occurrenceTwo.md) | Specifies the second of two occurrences the joint is between. |
| [parentComponent](AsBuiltJoint_parentComponent.md) | Returns the parent component that owns this AsBuiltJoint. |
| [timelineObject](AsBuiltJoint_timelineObject.md) | Returns the timeline object associated with this as-built joint. |
| [transform](AsBuiltJoint_transform.md) | Returns the position and orientation of the joint geometry associated with this as-built joint. This is returned as a 3D matrix which provides the origin and the X, Y, and Z axis vectors of the coordinate system. This property is especially useful in cases where the JointGeometry cannot be obtained. This can happen when the model has been modified in a way where the geometry used to create the joint is no longer available. |

## Accessed From

[AsBuiltJoint.createForAssemblyContext](AsBuiltJoint_createForAssemblyContext.md), [AsBuiltJoint.nativeObject](AsBuiltJoint_nativeObject.md), [AsBuiltJointList.item](AsBuiltJointList_item.md), [AsBuiltJointList.itemByName](AsBuiltJointList_itemByName.md), [AsBuiltJoints.add](AsBuiltJoints_add.md), [AsBuiltJoints.item](AsBuiltJoints_item.md), [AsBuiltJoints.itemByName](AsBuiltJoints_itemByName.md), [Component.allAsBuiltJoints](Component_allAsBuiltJoints.md), [FlatPatternComponent.allAsBuiltJoints](FlatPatternComponent_allAsBuiltJoints.md)

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |

## Version

Introduced in version September 2015  

