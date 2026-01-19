# ExtentDefinition Object

Derived from: [Base](Base.md) Object  

## Description

The base class for the various definition objects used to define the extent of a feature.

## Methods

| Name | Description |
|----|----|
| [classType](ExtentDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [isValid](ExtentDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ExtentDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFeature](ExtentDefinition_parentFeature.md) | Returns the parent feature that this definition is associated with. If this definition has been created statically and is not associated with a feature this property will return null. |

## Accessed From

[DraftFeature.draftDefinition](DraftFeature_draftDefinition.md), [ExtrudeFeature.extentOne](ExtrudeFeature_extentOne.md), [ExtrudeFeature.extentTwo](ExtrudeFeature_extentTwo.md), [ExtrudeFeature.startExtent](ExtrudeFeature_startExtent.md), [ExtrudeFeatureInput.extentOne](ExtrudeFeatureInput_extentOne.md), [ExtrudeFeatureInput.extentTwo](ExtrudeFeatureInput_extentTwo.md), [ExtrudeFeatureInput.startExtent](ExtrudeFeatureInput_startExtent.md), [HoleFeature.extentDefinition](HoleFeature_extentDefinition.md), [RevolveFeature.extentDefinition](RevolveFeature_extentDefinition.md)

## Derived Classes

[AllExtentDefinition](AllExtentDefinition.md), [AngleExtentDefinition](AngleExtentDefinition.md), [DistanceExtentDefinition](DistanceExtentDefinition.md), [FromEntityStartDefinition](FromEntityStartDefinition.md), [OffsetStartDefinition](OffsetStartDefinition.md), [OneSideToExtentDefinition](OneSideToExtentDefinition.md), [ProfilePlaneStartDefinition](ProfilePlaneStartDefinition.md), [SymmetricExtentDefinition](SymmetricExtentDefinition.md), [ThroughAllExtentDefinition](ThroughAllExtentDefinition.md), [ToEntityExtentDefinition](ToEntityExtentDefinition.md), [TwoSidesAngleExtentDefinition](TwoSidesAngleExtentDefinition.md), [TwoSidesDistanceExtentDefinition](TwoSidesDistanceExtentDefinition.md), [TwoSidesToExtentDefinition](TwoSidesToExtentDefinition.md)

## Version

Introduced in version August 2014  

