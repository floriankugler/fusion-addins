# Component.getPhysicalProperties Method

Parent Object: [Component](Component.md)  

## Description

Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this component.

## Syntax

"component_var" is a variable referencing a [Component](Component.md) object.

```python
# Uses no optional arguments.
returnValue = component_var.getPhysicalProperties()

# Uses optional arguments.
returnValue = component_var.getPhysicalProperties(accuracy)
```

## Return Value

| Type | Description |
|----|----|
| [PhysicalProperties](PhysicalProperties.md) | Returns a PhysicalProperties object that can be used to get the various physical property related values. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| accuracy | [CalculationAccuracy](CalculationAccuracy.md) | Specifies the desired level of computational accuracy of the property calculations. The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin. This is an optional argument whose default value is CalculationAccuracy.LowCalculationAccuracy. |

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version May 2016  

