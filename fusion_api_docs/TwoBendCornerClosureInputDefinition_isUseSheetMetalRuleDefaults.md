# TwoBendCornerClosureInputDefinition.isUseSheetMetalRuleDefaults Property

Parent Object: [TwoBendCornerClosureInputDefinition](TwoBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets whether to use default relief values from the Sheet Metal Rule. When true, all relief parameters (shape, size, and placement) are taken from the active Sheet Metal Rule, and any values set in twoBendReliefShape, twoBendReliefSize, and twoBendReliefPlacement properties are ignored. When false (default), the relief parameters must be explicitly set using the respective properties. The default value is false.

## Syntax

"twoBendCornerClosureInputDefinition_var" is a variable referencing a TwoBendCornerClosureInputDefinition object.  

```python
# Get the value of the property.
propertyValue = twoBendCornerClosureInputDefinition_var.isUseSheetMetalRuleDefaults

# Set the value of the property.
twoBendCornerClosureInputDefinition_var.isUseSheetMetalRuleDefaults = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2026  

