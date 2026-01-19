# ThreeBendCornerClosureFeatureDefinition.isUseSheetMetalRuleDefaults Property

Parent Object: [ThreeBendCornerClosureFeatureDefinition](ThreeBendCornerClosureFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets whether to use default values from the Sheet Metal Rule for all three-bend relief parameters (shape and radius).  

When set to true, the relief shape and radius are retrieved from the active Sheet Metal Rule. When set to false (default), the explicitly set values for these parameters are used.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

The default value is false.

## Syntax

"threeBendCornerClosureFeatureDefinition_var" is a variable referencing a ThreeBendCornerClosureFeatureDefinition object.  

```python
# Get the value of the property.
propertyValue = threeBendCornerClosureFeatureDefinition_var.isUseSheetMetalRuleDefaults

# Set the value of the property.
threeBendCornerClosureFeatureDefinition_var.isUseSheetMetalRuleDefaults = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2026  

