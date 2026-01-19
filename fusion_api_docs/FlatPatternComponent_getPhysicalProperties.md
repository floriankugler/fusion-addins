# FlatPatternComponent.getPhysicalProperties Method

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this component.

## Syntax

"flatPatternComponent_var" is a variable referencing a [FlatPatternComponent](FlatPatternComponent.md) object.

```python
# Uses no optional arguments.
returnValue = flatPatternComponent_var.getPhysicalProperties()

# Uses optional arguments.
returnValue = flatPatternComponent_var.getPhysicalProperties(accuracy)
```

## Return Value

| Type | Description |
|----|----|
| [PhysicalProperties](PhysicalProperties.md) | Returns a PhysicalProperties object that can be used to get the various physical property related values. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| accuracy | [CalculationAccuracy](CalculationAccuracy.md) | Specifies the desired level of computational accuracy of the property calculations. The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin. This is an optional argument whose default value is CalculationAccuracy.LowCalculationAccuracy. |

## Version

Introduced in version October 2022  

