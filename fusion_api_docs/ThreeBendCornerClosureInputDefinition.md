
Derived from: [CornerClosureInputDefinition](CornerClosureInputDefinition.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Defines the input properties required for creating a three-bend corner closure feature. This input definition provides a structured way to organize and validate the parameters before passing them to the setThreeBendCornerClosure method.

## Methods

| Name | Description |
|----|----|
| [classType](ThreeBendCornerClosureInputDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](ThreeBendCornerClosureInputDefinition_create.md) | Creates a ThreeBendCornerClosureParameters object that can be used to define parameters for a three-bend corner closure. Use properties on this object to set the relief shape, relief radius, miter gap, alignment settings, and bend transition type before passing it to the setThreeBendCornerClosure method. |

## Properties

| Name | Description |
| --- | --- |
| [bendTransition](ThreeBendCornerClosureInputDefinition_bendTransition.md) | Gets and sets the bend transition type for the corner closure. This determines how the bend transitions are handled at the corner intersection. The default value is TrimToBendCornerBendTransitionType. |
| [isExtendAligned](ThreeBendCornerClosureInputDefinition_isExtendAligned.md) | Gets and sets a value indicating whether the corner closure extends aligned to the edges. When true, the corner closure will extend in alignment with the adjacent edges. When false, the corner closure will use the default extension behavior. The default value is true. |
| [isUseSheetMetalRuleDefaults](ThreeBendCornerClosureInputDefinition_isUseSheetMetalRuleDefaults.md) | Gets and sets whether to use default relief values from the Sheet Metal Rule. When true, all relief parameters (shape and radius) are taken from the active Sheet Metal Rule, and any values set in threeBendReliefShape and threeBendReliefRadius properties are ignored. When false (default), the relief parameters must be explicitly set using the respective properties. The default value is false. |
| [isUseSheetMetalRuleMiterGap](ThreeBendCornerClosureInputDefinition_isUseSheetMetalRuleMiterGap.md) | Gets and sets whether to use the miter gap value from the Sheet Metal Rule. When true, the miter gap value is taken from the active Sheet Metal Rule and any value set in the miterGap property is ignored. When false (default), the behavior depends on the miterGap property: - If miterGap is set: uses the specified value - If miterGap is not set (null): uses the value from the Sheet Metal Rule as a fallback The default value is false. |
| [isValid](ThreeBendCornerClosureInputDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [miterGap](ThreeBendCornerClosureInputDefinition_miterGap.md) | Gets and sets the gap distance for the miter in the corner closure. This value defines the spacing between the sheets at the corner miter joint. If this property is not set (null) and useSheetMetalRuleMiterGap is false, the miter gap value will be taken from the Sheet Metal Rule as a fallback. |
| [objectType](ThreeBendCornerClosureInputDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [threeBendReliefRadius](ThreeBendCornerClosureInputDefinition_threeBendReliefRadius.md) | Gets and sets the radius of the three-bend relief. This parameter is only valid when the threeBendReliefShape is RoundWithRadiusCornerThreeBendReliefShapeType. For other relief shapes, this value is ignored. This property is ignored when useSheetMetalRuleDefaults is set to true. |
| [threeBendReliefShape](ThreeBendCornerClosureInputDefinition_threeBendReliefShape.md) | Gets and sets the relief shape for the three-bend corner. This defines the geometric shape used to relieve stress at the corner where three bends meet. This property is ignored when useSheetMetalRuleDefaults is set to true. The default value is RoundWithRadiusCornerThreeBendReliefShapeType. |

## Accessed From

[ThreeBendCornerClosureInputDefinition.create](ThreeBendCornerClosureInputDefinition_create.md)

## Version

Introduced in version January 2026  

