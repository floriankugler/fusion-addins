# DraftFeature.draftDefinition Property

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Gets the definition object that specifies how the draft is defined. Modifying the definition object will cause the draft to recompute. This can return either an AngleExtentDefinition or TwoSidesAngleExtentDefinition object. This property returns nothing in the case where the feature is non-parametric. Use this property to access the parameters controlling the draft and whether the draft is symmetric or not.

## Syntax

"draftFeature_var" is a variable referencing a DraftFeature object.  

```python
# Get the value of the property.
propertyValue = draftFeature_var.draftDefinition
```

## Property Value

This is a read only property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Version

Introduced in version January 2015  

