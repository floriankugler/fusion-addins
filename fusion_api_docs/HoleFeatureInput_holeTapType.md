# HoleFeatureInput.holeTapType Property

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Returns the current type of tap associated with this hole. When a new HoleFeatureInput is created, this will default to SimpleHoleTapType, which means the hole will not have any tap and will be a simple hole. You can set the tap type by using one of the methods to define the specific tap desired.

## Syntax

"holeFeatureInput_var" is a variable referencing a HoleFeatureInput object.  

```python
# Get the value of the property.
propertyValue = holeFeatureInput_var.holeTapType
```

## Property Value

This is a read only property whose value is a [HoleTapTypes](HoleTapTypes.md).

## Version

Introduced in version September 2025  

