# Joints Object

Derived from: [Base](Base.md) Object  

## Description

The collection of joints in this component. This provides access to all existing joints and supports the ability to create new joints.

## Methods

| Name | Description |
|----|----|
| [add](Joints_add.md) | Creates a new joint. |
| [addInferredJoint](Joints_addInferredJoint.md) | Creates a new inferred joint. |
| [classType](Joints_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createInferredJointInput](Joints_createInferredJointInput.md) | Creates a joint input to define an inferred joint. Use functionality on the returned InferredJointInput to define the input needed to infer a joint. |
| [createInput](Joints_createInput.md) | Creates a JointInput object, which is the API equivalent to the Joint command dialog. You you use methods and properties on the returned class to set the desired options, similar to providing input and setting options in the Joint command dialog. Once the settings are defined you call the Joints.add method passing in the JointInput object to create the actual joint. |
| [item](Joints_item.md) | Function that returns the specified joint using an index into the collection. |
| [itemByName](Joints_itemByName.md) | Function that returns the specified joint using a name. |

## Properties

| Name | Description |
| --- | --- |
| [count](Joints_count.md) | Returns number of joints in the collection. |
| [isValid](Joints_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Joints_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Component.joints](Component_joints.md), [FlatPatternComponent.joints](FlatPatternComponent_joints.md)

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

