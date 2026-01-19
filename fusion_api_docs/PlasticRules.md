# PlasticRules Object

Derived from: [Base](Base.md) Object  

## Description

A collection of plastic rules.

## Methods

| Name | Description |
|----|----|
| [addByCopy](PlasticRules_addByCopy.md) | Creates a new plastic rule by copying an existing rule. The new rule can then be edited to define the rule characteristics you want. |
| [classType](PlasticRules_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](PlasticRules_item.md) | Function that returns the specified plastic rule using an index into the collection. |
| [itemByName](PlasticRules_itemByName.md) | Function that returns the specified plastic rule using the name of the rule. |

## Properties

| Name | Description |
| --- | --- |
| [count](PlasticRules_count.md) | The number of plastic rules in the collection. |
| [isValid](PlasticRules_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PlasticRules_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Design.designPlasticRules](Design_designPlasticRules.md), [Design.libraryPlasticRules](Design_libraryPlasticRules.md), [FlatPatternProduct.designPlasticRules](FlatPatternProduct_designPlasticRules.md), [FlatPatternProduct.libraryPlasticRules](FlatPatternProduct_libraryPlasticRules.md), [WorkingModel.designPlasticRules](WorkingModel_designPlasticRules.md), [WorkingModel.libraryPlasticRules](WorkingModel_libraryPlasticRules.md)

## Version

Introduced in version January 2024  

