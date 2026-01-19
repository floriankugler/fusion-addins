
Derived from: [CornerClosureFeatureDefinition](CornerClosureFeatureDefinition.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The definition for a three bend corner closure.

## Methods

| Name | Description |
|----|----|
| [classType](ThreeBendCornerClosureFeatureDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [bendTransition](ThreeBendCornerClosureFeatureDefinition_bendTransition.md) | Gets and sets the bend transition type for the corner closure. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [dominantEdge](ThreeBendCornerClosureFeatureDefinition_dominantEdge.md) | Gets the dominant edge for the corner closure. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) After setting the edge, the definitionType property on CornerClosureFeature should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered. |
| [isExtendAligned](ThreeBendCornerClosureFeatureDefinition_isExtendAligned.md) | Gets and sets whether the corner closure extends aligned to the edges. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |
| [isUseSheetMetalRuleDefaults](ThreeBendCornerClosureFeatureDefinition_isUseSheetMetalRuleDefaults.md) | Gets and sets whether to use default values from the Sheet Metal Rule for all three-bend relief parameters (shape and radius). When set to true, the relief shape and radius are retrieved from the active Sheet Metal Rule. When set to false (default), the explicitly set values for these parameters are used. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) The default value is false. |
| [isUseSheetMetalRuleMiterGap](ThreeBendCornerClosureFeatureDefinition_isUseSheetMetalRuleMiterGap.md) | Gets and sets whether to use the miter gap value from the Sheet Metal Rule. When set to true, the miter gap value is retrieved from the active Sheet Metal Rule. When set to false (default), the explicitly set miterGap value is used. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) The default value is false. |
| [isValid](ThreeBendCornerClosureFeatureDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [miterGap](ThreeBendCornerClosureFeatureDefinition_miterGap.md) | Gets the miter gap for the corner closure. |
| [objectType](ThreeBendCornerClosureFeatureDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [submissiveEdge](ThreeBendCornerClosureFeatureDefinition_submissiveEdge.md) | Gets and sets the submissive edge for the corner closure. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) After setting the edge, the definitionType property on CornerClosureFeature should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered. |
| [threeBendReliefRadius](ThreeBendCornerClosureFeatureDefinition_threeBendReliefRadius.md) | Gets the radius of the three-bend relief. |
| [threeBendReliefShape](ThreeBendCornerClosureFeatureDefinition_threeBendReliefShape.md) | Gets and sets the relief shape for the three-bend corner. To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True) |

## Version

Introduced in version January 2026  

