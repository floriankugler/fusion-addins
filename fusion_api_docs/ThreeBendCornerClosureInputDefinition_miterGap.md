# ThreeBendCornerClosureInputDefinition.miterGap Property

Parent Object: [ThreeBendCornerClosureInputDefinition](ThreeBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the gap distance for the miter in the corner closure. This value defines the spacing between the sheets at the corner miter joint. If this property is not set (null) and useSheetMetalRuleMiterGap is false, the miter gap value will be taken from the Sheet Metal Rule as a fallback.

## Syntax

"threeBendCornerClosureInputDefinition_var" is a variable referencing a ThreeBendCornerClosureInputDefinition object.  

```python
# Get the value of the property.
propertyValue = threeBendCornerClosureInputDefinition_var.miterGap

# Set the value of the property.
threeBendCornerClosureInputDefinition_var.miterGap = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2026  

