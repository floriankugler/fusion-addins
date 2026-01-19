# ChamferFeature.chamferTypeDefinition Property

Parent Object: [ChamferFeature](ChamferFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets the definition object that is defining the type of chamfer. Modifying the definition object will cause the chamfer to recompute. Various types of definition objects can be returned depending on how the chamfer is defined. The ChamferType property can be used to determine which type of definition will be returned. This property returns nothing in the case where the feature is non-parametric.

## Syntax

"chamferFeature_var" is a variable referencing a ChamferFeature object.  

```python
# Get the value of the property.
propertyValue = chamferFeature_var.chamferTypeDefinition
```

## Property Value

This is a read only property whose value is a [ChamferTypeDefinition](ChamferTypeDefinition.md).

## Version

Introduced in version November 2014  
Retired in version December 2020  

