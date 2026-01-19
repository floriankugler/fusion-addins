# FullRoundFilletFaceSet Object

Derived from: [Base](Base.md) Object  

## Description

The class for the full round fillet face set.

## Methods

| Name | Description |
| --- | --- |
| [classType](FullRoundFilletFaceSet_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](FullRoundFilletFaceSet_deleteMe.md) | Deletes the full round fillet face set from the fillet. When this face set is associated with an existing fillet feature, to use this method you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |

## Properties

| Name | Description |
| --- | --- |
| [areAutomaticSideFaces](FullRoundFilletFaceSet_areAutomaticSideFaces.md) | Property that returns a boolean value indicating whether the side faces are used as automatically inferred side faces. It returns true indicating that the side faces are not being shown in the dialog when the user edits the feature. Calling the setSideFaces method will cause this property to be changed to false. |
| [centerFace](FullRoundFilletFaceSet_centerFace.md) | Gets the center face associated with this full round fillet face set. When a center face has tangentially connected faces then all the tangentially connected faces will be filleted automatically. When this face set is associated with an existing fillet feature, to get the center face you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [isValid](FullRoundFilletFaceSet_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](FullRoundFilletFaceSet_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [sideOneFaces](FullRoundFilletFaceSet_sideOneFaces.md) | Gets the side one faces. When this face set is associated with an existing fillet feature, to get the side one faces you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |
| [sideTwoFaces](FullRoundFilletFaceSet_sideTwoFaces.md) | Gets the side two faces. When this face set is associated with an existing fillet feature, to get the side two faces you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True). |

## Accessed From

[FullRoundFilletFaceSets.add](FullRoundFilletFaceSets_add.md), [FullRoundFilletFaceSets.item](FullRoundFilletFaceSets_item.md)

## Version

Introduced in version September 2025  

