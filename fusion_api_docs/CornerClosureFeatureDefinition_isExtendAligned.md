# CornerClosureFeatureDefinition.isExtendAligned Property

Parent Object: [CornerClosureFeatureDefinition](CornerClosureFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets whether the corner closure extends aligned to the edges.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"cornerClosureFeatureDefinition_var" is a variable referencing a CornerClosureFeatureDefinition object.  

```python
# Get the value of the property.
propertyValue = cornerClosureFeatureDefinition_var.isExtendAligned

# Set the value of the property.
cornerClosureFeatureDefinition_var.isExtendAligned = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2026  

