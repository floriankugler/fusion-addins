# ThreeBendCornerClosureInputDefinition.isUseSheetMetalRuleMiterGap Property

Parent Object: [ThreeBendCornerClosureInputDefinition](ThreeBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets whether to use the miter gap value from the Sheet Metal Rule. When true, the miter gap value is taken from the active Sheet Metal Rule and any value set in the miterGap property is ignored. When false (default), the behavior depends on the miterGap property: - If miterGap is set: uses the specified value - If miterGap is not set (null): uses the value from the Sheet Metal Rule as a fallback The default value is false.

## Syntax

"threeBendCornerClosureInputDefinition_var" is a variable referencing a ThreeBendCornerClosureInputDefinition object.  

```python
# Get the value of the property.
propertyValue = threeBendCornerClosureInputDefinition_var.isUseSheetMetalRuleMiterGap

# Set the value of the property.
threeBendCornerClosureInputDefinition_var.isUseSheetMetalRuleMiterGap = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2026  

