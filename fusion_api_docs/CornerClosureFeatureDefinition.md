
Derived from: [Base](Base.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

A Base class to return the information used to define the CornerClosureFeature.

## Methods

| Name | Description |
|----|----|
| [classType](CornerClosureFeatureDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [bendTransition](CornerClosureFeatureDefinition_bendTransition.md) | Gets and sets the bend transition type for the corner closure. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [dominantEdge](CornerClosureFeatureDefinition_dominantEdge.md) | Gets the dominant edge for the corner closure. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) After setting the edge, the definitionType property on CornerClosureFeature should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered. |
| [isExtendAligned](CornerClosureFeatureDefinition_isExtendAligned.md) | Gets and sets whether the corner closure extends aligned to the edges. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isValid](CornerClosureFeatureDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [miterGap](CornerClosureFeatureDefinition_miterGap.md) | Gets the miter gap for the corner closure. |
| [objectType](CornerClosureFeatureDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [submissiveEdge](CornerClosureFeatureDefinition_submissiveEdge.md) | Gets and sets the submissive edge for the corner closure. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) After setting the edge, the definitionType property on CornerClosureFeature should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered. |

## Accessed From

[CornerClosureFeature.definition](CornerClosureFeature_definition.md)

## Derived Classes

[ThreeBendCornerClosureFeatureDefinition](ThreeBendCornerClosureFeatureDefinition.md), [TwoBendCornerClosureFeatureDefinition](TwoBendCornerClosureFeatureDefinition.md)

## Version

Introduced in version January 2026  

