# SketchTextDefinition Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the classes that define how text can be defined.

## Methods

| Name | Description |
|----|----|
| [classType](SketchTextDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](SketchTextDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](SketchTextDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentSketchText](SketchTextDefinition_parentSketchText.md) | Returns the SketchText object this definition is associated with. This property will return null in the case the definition object was obtained from a SketchTextInput object because the SketchText object does not yet exist. |

## Accessed From

[SketchText.definition](SketchText_definition.md), [SketchTextInput.definition](SketchTextInput_definition.md)

## Derived Classes

[AlongPathTextDefinition](AlongPathTextDefinition.md), [FitOnPathTextDefintion](FitOnPathTextDefintion.md), [MultiLineTextDefinition](MultiLineTextDefinition.md)

## Version

Introduced in version December 2020  

