# HoleFeature.extentDefinition Property

Parent Object: [HoleFeature](HoleFeature.md)  

## Description

Gets the definition object that is defining the extent of the hole. Modifying the definition object will cause the hole to recompute. The extent type of a hole is currently limited to a distance extent.

## Syntax

"holeFeature_var" is a variable referencing a HoleFeature object.  

```python
# Get the value of the property.
propertyValue = holeFeature_var.extentDefinition
```

## Property Value

This is a read only property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Version

Introduced in version August 2014  

