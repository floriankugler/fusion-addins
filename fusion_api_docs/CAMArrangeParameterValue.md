# CAMArrangeParameterValue Object

Derived from: [ParameterValue](ParameterValue.md) Object  

## Description

A parameter value that is a CAMArrangeParameterValue. The user needs to set the parameter anew via the API after a model update or after the ArrangeSelections returned by getArrangeSelections() have been edited.

## Methods

| Name | Description |
|----|----|
| [applyArrangeSelections](CAMArrangeParameterValue_applyArrangeSelections.md) | Set the values of the parameter as a collection of CadObjects. |
| [classType](CAMArrangeParameterValue_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [getArrangeSelections](CAMArrangeParameterValue_getArrangeSelections.md) | Get the values of the parameter as a collection of CadObjects, which currently consist of occurrences. |

## Properties

| Name | Description |
| --- | --- |
| [isValid](CAMArrangeParameterValue_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMArrangeParameterValue_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](CAMArrangeParameterValue_parent.md) | Get the parameter object that the value is associated with. |

## Version

Introduced in version March 2024  

