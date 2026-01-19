# PhysicalProperties.accuracy Property

Parent Object: [PhysicalProperties](PhysicalProperties.md)  

## Description

Returns the accuracy that was used for the calculation.

## Syntax

"physicalProperties_var" is a variable referencing a PhysicalProperties object.  

```python
# Get the value of the property.
propertyValue = physicalProperties_var.accuracy
```

## Property Value

This is a read only property whose value is a [CalculationAccuracy](CalculationAccuracy.md).

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version May 2016  

