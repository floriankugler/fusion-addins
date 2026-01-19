
Derived from: [HemFeatureDefinition](HemFeatureDefinition.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The definition for a rope hem.

## Methods

| Name | Description |
|----|----|
| [classType](RopeHemFeatureDefinition_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [bendPositionType](RopeHemFeatureDefinition_bendPositionType.md) | Gets the bend position type for a hem. |
| [gap](RopeHemFeatureDefinition_gap.md) | Gets the gap for a rope hem. |
| [hemEdge](RopeHemFeatureDefinition_hemEdge.md) | Gets and sets the input edge for a hem |
| [isFlipped](RopeHemFeatureDefinition_isFlipped.md) | Gets the flip direction for an open hem. |
| [isValid](RopeHemFeatureDefinition_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [length](RopeHemFeatureDefinition_length.md) | Gets the length for a rope hem. |
| [objectType](RopeHemFeatureDefinition_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [radius](RopeHemFeatureDefinition_radius.md) | Gets the radius for a rope hem. |

## Version

Introduced in version September 2025  

