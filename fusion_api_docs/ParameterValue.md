# ParameterValue Object

Derived from: [Base](Base.md) Object  

## Description

Base class for representing the value of a parameter. Subclasses implement value handling for available parameter types.

## Methods

| Name | Description |
|----|----|
| [classType](ParameterValue_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ParameterValue_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ParameterValue_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](ParameterValue_parent.md) | Get the parameter object that the value is associated with. |

## Accessed From

[CAMParameter.value](CAMParameter_value.md)

## Derived Classes

[BooleanParameterValue](BooleanParameterValue.md), [CadContours2dParameterValue](CadContours2dParameterValue.md), [CadMachineAvoidGroupsParameterValue](CadMachineAvoidGroupsParameterValue.md), [CadObjectParameterValue](CadObjectParameterValue.md), [CAMArrangeParameterValue](CAMArrangeParameterValue.md), [ChoiceParameterValue](ChoiceParameterValue.md), [FloatParameterValue](FloatParameterValue.md), [IntegerParameterValue](IntegerParameterValue.md), [StringParameterValue](StringParameterValue.md)

## Version

Introduced in version September 2021  

