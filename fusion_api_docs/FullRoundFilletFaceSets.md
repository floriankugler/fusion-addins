# FullRoundFilletFaceSets Object

Derived from: [Base](Base.md) Object  

## Description

Collection that provides access to all existing full round fillet face sets associated with a full round fillet feature or a FullRoundFilletFeatureInput object, and allows adding new full round fillet face sets.

## Methods

| Name | Description |
| --- | --- |
| [add](FullRoundFilletFaceSets_add.md) | Adds a set of faces to be filleted to the full round fillet feature. When this face set is associated with an existing fillet feature, to use this method you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [classType](FullRoundFilletFaceSets_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [item](FullRoundFilletFaceSets_item.md) | Function that returns the specified full round fillet face set using an index into the collection. |

## Properties

| Name | Description |
| --- | --- |
| [count](FullRoundFilletFaceSets_count.md) | The number of full round fillet face sets in the collection. |
| [isValid](FullRoundFilletFaceSets_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FullRoundFilletFaceSets_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[FilletFeature.fullRoundFilletFaceSets](FilletFeature_fullRoundFilletFaceSets.md), [FullRoundFilletFeatureInput.faceSets](FullRoundFilletFeatureInput_faceSets.md)

## Version

Introduced in version September 2025  

