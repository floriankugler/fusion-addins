# TwoBendCornerClosureInputDefinition.bendTransition Property

Parent Object: [TwoBendCornerClosureInputDefinition](TwoBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the bend transition type for the corner closure. This determines how the bend transitions are handled at the corner intersection. The default value is TrimToBendCornerBendTransitionType.

## Syntax

"twoBendCornerClosureInputDefinition_var" is a variable referencing a TwoBendCornerClosureInputDefinition object.  

```python
# Get the value of the property.
propertyValue = twoBendCornerClosureInputDefinition_var.bendTransition

# Set the value of the property.
twoBendCornerClosureInputDefinition_var.bendTransition = propertyValue
```

## Property Value

This is a read/write property whose value is a [CornerBendTransitionTypes](CornerBendTransitionTypes.md).

## Version

Introduced in version January 2026  

