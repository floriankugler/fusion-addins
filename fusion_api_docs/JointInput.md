# JointInput Object

Derived from: [Base](Base.md) Object  

## Description

Defines all of the information required to create a new joint. This object provides equivalent functionality to the Joint command dialog in that it gathers the required information to create a joint.

## Methods

| Name | Description |
|----|----|
| [classType](JointInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [setAsBallJointMotion](JointInput_setAsBallJointMotion.md) | Defines the relationship between the two joint geometries as a ball joint. |
| [setAsCylindricalJointMotion](JointInput_setAsCylindricalJointMotion.md) | Defines the relationship between the two joint geometries as a cylindrical joint. |
| [setAsPinSlotJointMotion](JointInput_setAsPinSlotJointMotion.md) | Defines the relationship between the two joint geometries as a pin-slot joint. |
| [setAsPlanarJointMotion](JointInput_setAsPlanarJointMotion.md) | Defines the relationship between the two joint geometries as a planar joint. |
| [setAsRevoluteJointMotion](JointInput_setAsRevoluteJointMotion.md) | Defines the relationship between the two joint geometries as a revolute joint. |
| [setAsRigidJointMotion](JointInput_setAsRigidJointMotion.md) | Defines the relationship between the two joint geometries as a rigid joint. |
| [setAsSliderJointMotion](JointInput_setAsSliderJointMotion.md) | Defines the relationship between the two joint geometries as a slider joint. |

## Properties

| Name | Description |
| --- | --- |
| [angle](JointInput_angle.md) | Specifies the angle between two input geometries. This is effectively the angle between the two primary axes of the input geometries. When a new JointInput object is created, this value defaults to zero. When the joint is created this will become the value of the parameter that controls the joint angle. When using a real value to define the angle, the value is in radians. When using a string the expression is evaluated using the document default units for angles. |
| [geometryOrOriginOne](JointInput_geometryOrOriginOne.md) | Gets and sets the first JointGeometry or JointOrigin for this joint. |
| [geometryOrOriginTwo](JointInput_geometryOrOriginTwo.md) | Gets and sets the second JointGeometry or JointOrigin for this joint. |
| [isFlipped](JointInput_isFlipped.md) | Gets and sets if the joint direction is flipped or not. This is effectively specifying if the third axis of the two input geometries is facing (false) or opposed (true). |
| [isValid](JointInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [jointMotion](JointInput_jointMotion.md) | Returns an object derived from JointMotion that defines how the motion between the two joint geometries is defined. |
| [objectType](JointInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [offset](JointInput_offset.md) | Specifies the offset between two input geometries. This is effectively the offset distance between the two planes defined by the primary and secondary axes of the input geometries. When a new JointInput object is created, this value defaults to zero. When the joint is created this will become the value of the parameter that controls the joint offset. When using a real value to define the offset, the value is in centimeters. When using a string the expression is evaluated using the document default units for distance. |

## Accessed From

[Joints.createInput](Joints_createInput.md)

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

