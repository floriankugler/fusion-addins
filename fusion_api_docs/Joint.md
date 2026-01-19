# Joint Object

Derived from: [Base](Base.md) Object  

## Description

A joint in a design.

## Methods

| Name | Description |
| --- | --- |
| [classType](Joint_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createForAssemblyContext](Joint_createForAssemblyContext.md) | Creates or returns a proxy for the native object - i.e. a new object that represents this object but adds the assembly context defined by the input occurrence. |
| [deleteMe](Joint_deleteMe.md) | Deletes this joint. |
| [setAsBallJointMotion](Joint_setAsBallJointMotion.md) | Redefines the relationship between the two joint geometries as a ball joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [setAsCylindricalJointMotion](Joint_setAsCylindricalJointMotion.md) | Redefines the relationship between the two joint geometries as a cylindrical joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [setAsPinSlotJointMotion](Joint_setAsPinSlotJointMotion.md) | Redefines the relationship between the two joint geometries as a pin-slot joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [setAsPlanarJointMotion](Joint_setAsPlanarJointMotion.md) | Redefines the relationship between the two joint geometries as a planar joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [setAsRevoluteJointMotion](Joint_setAsRevoluteJointMotion.md) | Redefines the relationship between the two joint geometries as a revolute joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [setAsRigidJointMotion](Joint_setAsRigidJointMotion.md) | Redefines the relationship between the two joint geometries as a rigid joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [setAsSliderJointMotion](Joint_setAsSliderJointMotion.md) | Redefines the relationship between the two joint geometries as a slider joint. This method will fail in the case where the jointType property returns InferredJointType. To use this method, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |

## Properties

| Name | Description |
| --- | --- |
| [angle](Joint_angle.md) | Returns the parameter controlling the angle between the two input geometries. This is effectively the angle between the two primary axes of the two joint geometries. This property will return null in the case where the jointType property returns InferredJointType. |
| [assemblyContext](Joint_assemblyContext.md) | Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object. |
| [attributes](Joint_attributes.md) | Returns the collection of attributes associated with this joint. |
| [entityToken](Joint_entityToken.md) | Returns a token for the Joint object. This can be saved and used at a later time with the Design.findEntityByToken method to get back the same joint. When using entity tokens it's important to understand that the token string returned for a specific entity can be different over time. However, even if you have two different token strings that were obtained from the same entity, when you use findEntityByToken they will both return the same entity. Because of that you should never compare entity tokens as way to determine what the token represents. Instead, you need to use the findEntityByToken method to get the two entities identified by the tokens and then compare them. |
| [errorOrWarningMessage](Joint_errorOrWarningMessage.md) | Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string. |
| [geometricRelationships](Joint_geometricRelationships.md) | Returns the set of geometric relationships that were used to infer this joint. This property is only valid when the jointType property returns InferredJointType. Otherwise, it returns null. |
| [geometryOneTransform](Joint_geometryOneTransform.md) | Returns the position and orientation of the joint geometry associated with the first occurrence. This is returned as a 3D matrix which provides the origin and the X, Y, and Z axis vectors of the coordinate system. This property is especially useful in cases where the JointGeometry cannot be obtained. This can happen when the model has been modified in a way where the geometry used to create the joint is no longer available. This property will return null in the case where the jointType property returns InferredJointType. |
| [geometryOrOriginOne](Joint_geometryOrOriginOne.md) | Gets and sets the first JointGeometry or JointOrigin for this joint. If the JointType is InferredJointType, this property will return null when queried and will fail if it set. To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [geometryOrOriginTwo](Joint_geometryOrOriginTwo.md) | Gets and sets the second JointGeometry or JointOrigin for this joint. If the JointType is InferredJointType, this property will return null when queried and will fail if it set. To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) |
| [geometryTwoTransform](Joint_geometryTwoTransform.md) | Returns the position and orientation of the joint geometry associated with the second occurrence. This is returned as a 3D matrix which provides the origin and the X, Y, and Z axis vectors of the coordinate system. This property is especially useful in cases where the JointGeometry cannot be obtained. This can happen when the model has been modified in a way where the geometry used to create the joint is no longer available. This property will return null in the case where the jointType property returns InferredJointType. |
| [healthState](Joint_healthState.md) | Returns the current health state of the joint. |
| [isFlipped](Joint_isFlipped.md) | Gets and sets if the joint direction is flipped or not. This is effectively specifying if the third axis of the two input geometries is facing (false) or opposed (true). To set this property, you need to position the timeline marker to immediately before this joint. This can be accomplished using the following code: thisJoint.timelineObject.rollTo(True) The value of this property should be ignored in the case where the jointType property returns InferredJointType. |
| [isLightBulbOn](Joint_isLightBulbOn.md) | Gets and sets if the light bulb of this joint as displayed in the browser is on or off. A joint will only be visible if the light bulb is switched on. However, the light bulb can be on and the joint still invisible if a higher level occurrence in the assembly context is not visible because its light bulb is off or the joints folder is light bulb is off. |
| [isLocked](Joint_isLocked.md) | Gets and sets if the joint is locked. |
| [isSuppressed](Joint_isSuppressed.md) | Gets and sets if this joint is suppressed. |
| [isValid](Joint_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [isVisible](Joint_isVisible.md) | Gets whether the joint is visible. To change the visibility see the isLightBulbOn property. This property is affected by the assembly context. |
| [jointMotion](Joint_jointMotion.md) | Returns a JointMotion object that defines the motion relationship between the two geometries. This property will return null in the case where the jointType property returns InferredJointType. |
| [motionLinks](Joint_motionLinks.md) | Returns the MotionLink objects that this joint is involved in. |
| [name](Joint_name.md) | Gets and sets the name of the joint. |
| [nativeObject](Joint_nativeObject.md) | The NativeObject is the object outside the context of an assembly and in the context of it's parent component. Returns null in the case where this object is not in the context of an assembly but is already the native object. |
| [objectType](Joint_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [occurrenceOne](Joint_occurrenceOne.md) | Returns the first of two occurrences that this joint defines a relationship between. This is the occurrence that can also be found through the geometryOrOriginOne property. |
| [occurrenceTwo](Joint_occurrenceTwo.md) | Returns the first of two occurrences that this joint defines a relationship between. This is the occurrence that can also be found through the geometryOrOriginTwo property. |
| [offset](Joint_offset.md) | Returns the parameter controlling the offset between the two input geometries. This is effectively the offset distance between the two planes defined by the primary and secondary axes of the input geometries or the offset along the tertiary axis (z axis) of the joint. This property will return null in the case where the jointType property returns InferredJointType. |
| [offsetX](Joint_offsetX.md) | Returns the parameter controlling the offset along the primary axis (x axis) of the joint. To edit this value, get the parameter and use one of its properties to edit the value. This property will return null in the case where the jointType property returns InferredJointType. |
| [offsetY](Joint_offsetY.md) | Returns the parameter controlling the offset along the primary axis (y axis) of the joint. To edit this value, get the parameter and use one of its properties to edit the value. This property will return null in the case where the jointType property returns InferredJointType. |
| [parentComponent](Joint_parentComponent.md) | Returns the parent component that owns this joint. |
| [timelineObject](Joint_timelineObject.md) | Returns the timeline object associated with this joint. |

## Accessed From

[Component.allJoints](Component_allJoints.md), [FlatPatternComponent.allJoints](FlatPatternComponent_allJoints.md), [Joint.createForAssemblyContext](Joint_createForAssemblyContext.md), [Joint.nativeObject](Joint_nativeObject.md), [JointList.item](JointList_item.md), [JointList.itemByName](JointList_itemByName.md), [Joints.add](Joints_add.md), [Joints.addInferredJoint](Joints_addInferredJoint.md), [Joints.item](Joints_item.md), [Joints.itemByName](Joints_itemByName.md)

## Samples

| Name | Description |
|----|----|
| [BallJointMotion API Sample](BallJointMotionSample_Sample.md) | Demonstrates creating a joint with ball joint motion |
| [CylindricalJointMotion API Sample](CylindricalJointMotionSample_Sample.md) | Demonstrates creating a joint with cylindrical joint motion. |
| [Joint API Sample](JointSample_Sample.md) | Demonstrates creating a new joint. |
| [Pin Slot Joint Motion API Sample](PinSlotJointMotionSample_Sample.md) | Demonstrates creating a joint with pin slot joint motion |
| [Planar Joint Motion API Sample](PlanarJointMotionSample_Sample.md) | Demonstrates creating a joint with planar joint motion |
| [RevoluteJointMotion API Sample](RevoluteJointMotionSample_Sample.md) | Demonstrates creating a joint with revolute joint motion. |
| [SliderJointMotion API Sample](SliderJointMotionSample_Sample.md) | Demonstrates creating a joint with slider joint motion. |

## Version

Introduced in version July 2015  

