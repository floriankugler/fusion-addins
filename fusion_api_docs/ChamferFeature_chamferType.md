# ChamferFeature.chamferType Property

Parent Object: [ChamferFeature](ChamferFeature.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets an enum indicating how the chamfer was defined. The valid return values are EqualDistanceType, TwoDistancesType and DistanceAndAngleType. This property returns nothing in the case where the feature is non-parametric.

## Syntax

"chamferFeature_var" is a variable referencing a ChamferFeature object.  

```python
# Get the value of the property.
propertyValue = chamferFeature_var.chamferType
```

## Property Value

This is a read only property whose value is a [ChamferTypes](ChamferTypes.md).

## Version

Introduced in version November 2014  
Retired in version December 2020  

