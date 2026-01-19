# ThreeBendCornerClosureInputDefinition.threeBendReliefRadius Property

Parent Object: [ThreeBendCornerClosureInputDefinition](ThreeBendCornerClosureInputDefinition.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets the radius of the three-bend relief. This parameter is only valid when the threeBendReliefShape is RoundWithRadiusCornerThreeBendReliefShapeType. For other relief shapes, this value is ignored. This property is ignored when useSheetMetalRuleDefaults is set to true.

## Syntax

"threeBendCornerClosureInputDefinition_var" is a variable referencing a ThreeBendCornerClosureInputDefinition object.  

```python
# Get the value of the property.
propertyValue = threeBendCornerClosureInputDefinition_var.threeBendReliefRadius

# Set the value of the property.
threeBendCornerClosureInputDefinition_var.threeBendReliefRadius = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2026  

