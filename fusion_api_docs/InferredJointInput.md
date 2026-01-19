
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Defines all of the information required to create a new inferred joint. This object provides equivalent functionality to the Joint command dialog, gathering the required information to create an inferred joint.

## Methods

| Name | Description |
|----|----|
| [classType](InferredJointInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [geometricRelationships](InferredJointInput_geometricRelationships.md) | Returns the collection object used to define the geometric relationships from which the joint will be inferred. A geometric relationship defines several things: the pair of entities, if the relationship is flipped, if it defines a mating alignment or an angle, and the value of the offset or angle. |
| [isValid](InferredJointInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](InferredJointInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Joints.createInferredJointInput](Joints_createInferredJointInput.md)

## Version

Introduced in version July 2025  

