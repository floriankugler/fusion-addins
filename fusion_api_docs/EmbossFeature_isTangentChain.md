# EmbossFeature.isTangentChain Property

Parent Object: [EmbossFeature](EmbossFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets whether any faces that are tangentially connected to any of the input faces will also be used.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"embossFeature_var" is a variable referencing an EmbossFeature object.  

```python
# Get the value of the property.
propertyValue = embossFeature_var.isTangentChain

# Set the value of the property.
embossFeature_var.isTangentChain = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2025  

