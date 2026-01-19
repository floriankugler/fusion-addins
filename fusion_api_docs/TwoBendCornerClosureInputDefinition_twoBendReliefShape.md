# TwoBendCornerClosureInputDefinition.twoBendReliefShape Property

Parent Object: [TwoBendCornerClosureInputDefinition](TwoBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the relief shape for the two-bend corner. This defines the geometric shape used to relieve stress at the corner where two bends meet. This property is ignored when useSheetMetalRuleDefaults is set to true. The default value is RoundCornerTwoBendReliefShapeType.

## Syntax

"twoBendCornerClosureInputDefinition_var" is a variable referencing a TwoBendCornerClosureInputDefinition object.  

```python
# Get the value of the property.
propertyValue = twoBendCornerClosureInputDefinition_var.twoBendReliefShape

# Set the value of the property.
twoBendCornerClosureInputDefinition_var.twoBendReliefShape = propertyValue
```

## Property Value

This is a read/write property whose value is a [CornerTwoBendReliefShapeTypes](CornerTwoBendReliefShapeTypes.md).

## Version

Introduced in version January 2026  

