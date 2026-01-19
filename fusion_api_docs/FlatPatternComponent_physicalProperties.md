# FlatPatternComponent.physicalProperties Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this component. Property values will be calculated using the 'LowCalculationAccuracy' setting when using this property to get the PhysicalProperties object. To specify a higher calculation tolerance, use the getPhysicalProperties method instead.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.physicalProperties
```

## Property Value

This is a read only property whose value is a [PhysicalProperties](PhysicalProperties.md).

## Version

Introduced in version October 2022  

