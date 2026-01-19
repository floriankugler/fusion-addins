# ArrangeDefinitionInput Object

Derived from: [Base](Base.md) Object  

## Description

The ArrangeDefinition object is the base class for the ArrangeDefinition2D and ArrangeDefinition3D objects. It provides access to the information that defines an existing Arrange feature.

## Methods

| Name | Description |
|----|----|
| [classType](ArrangeDefinitionInput_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isCreateCopies](ArrangeDefinitionInput_isCreateCopies.md) | Gets and set if the original components will be moved or copied to create the arrangement. This defaults to true. |
| [isValid](ArrangeDefinitionInput_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ArrangeDefinitionInput_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [solverType](ArrangeDefinitionInput_solverType.md) | Gets the type of arrange feature defined by this definition. |

## Accessed From

[ArrangeFeatureInput.definition](ArrangeFeatureInput_definition.md)

## Derived Classes

[ArrangeDefinition2DInput](ArrangeDefinition2DInput.md), [ArrangeDefinition3DInput](ArrangeDefinition3DInput.md)

## Version

Introduced in version January 2025  

