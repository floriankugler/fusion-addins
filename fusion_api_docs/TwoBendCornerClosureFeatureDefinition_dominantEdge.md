# TwoBendCornerClosureFeatureDefinition.dominantEdge Property

Parent Object: [TwoBendCornerClosureFeatureDefinition](TwoBendCornerClosureFeatureDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets the dominant edge for the corner closure.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)  

After setting the edge, the definitionType property on CornerClosureFeature should be examined to determine whether the corner is two-bend or three-bend, as after the setting another edge the type of corner might be altered.

## Syntax

"twoBendCornerClosureFeatureDefinition_var" is a variable referencing a TwoBendCornerClosureFeatureDefinition object.  

```python
# Get the value of the property.
propertyValue = twoBendCornerClosureFeatureDefinition_var.dominantEdge

# Set the value of the property.
twoBendCornerClosureFeatureDefinition_var.dominantEdge = propertyValue
```

## Property Value

This is a read/write property whose value is a [BRepEdge](BRepEdge.md).

## Version

Introduced in version January 2026  

