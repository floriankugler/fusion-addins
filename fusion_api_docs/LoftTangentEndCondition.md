# LoftTangentEndCondition Object

Derived from: [LoftEndCondition](LoftEndCondition.md) Object  

## Description

Represents a "Tangent" loft end condition.

## Methods

| Name | Description |
|----|----|
| [classType](LoftTangentEndCondition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](LoftTangentEndCondition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](LoftTangentEndCondition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentLoftSection](LoftTangentEndCondition_parentLoftSection.md) | Returns the parent loft section. |
| [weight](LoftTangentEndCondition_weight.md) | Gets the valueInput or Parameter that defines the weight of the loft. If this object was obtained from a LoftFeatureInput object then this will return a valueInput object with the initial value provided. If this object was obtained from an exiting LoftFeature then it returns a Parameter. In the case of a parameter, to change the weight, edit the value of the associated parameter. |

## Version

Introduced in version August 2016  

