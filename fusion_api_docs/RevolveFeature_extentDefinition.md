# RevolveFeature.extentDefinition Property

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Gets the definition object that is defining the extent of the revolve. Modifying the definition object will cause the revolve to recompute. Various types of objects can be returned depending on the type of extent currently defined for the revolve. This property returns nothing in the case where the feature is non-parametric.

## Syntax

"revolveFeature_var" is a variable referencing a RevolveFeature object.  

```python
# Get the value of the property.
propertyValue = revolveFeature_var.extentDefinition
```

## Property Value

This is a read only property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Version

Introduced in version August 2014  

