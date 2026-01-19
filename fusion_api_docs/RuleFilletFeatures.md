# RuleFilletFeatures Object

Derived from: [Base](Base.md) Object  

## Description

This object is retired. See more information in the 'Remarks' section below.  

This object is obsolete. You should use the FilletFeatures to access the rule fillet features. The FilletFeature.filletFeatureType can be used to determine if a FilletFeature is a rule fillet feature or not.

## Remarks

Collection that provides access to all of the existing rule fillet features in a design.

## Methods

| Name | Description |
|----|----|
| [classType](RuleFilletFeatures_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](RuleFilletFeatures_item.md) | Function that returns the specified rule fillet feature using an index into the collection. |
| [itemByName](RuleFilletFeatures_itemByName.md) | Function that returns the specified rule fillet feature using the name of the feature. |

## Properties

| Name | Description |
| --- | --- |
| [count](RuleFilletFeatures_count.md) | The number of rule fillet features in the collection. |
| [isValid](RuleFilletFeatures_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](RuleFilletFeatures_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[Features.ruleFilletFeatures](Features_ruleFilletFeatures.md)

## Version

Introduced in version September 2015  

