# Component.physicalProperties Property

Parent Object: [Component](Component.md)  

## Description

Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this component. Property values will be calculated using the 'LowCalculationAccuracy' setting when using this property to get the PhysicalProperties object. To specify a higher calculation tolerance, use the getPhysicalProperties method instead.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.physicalProperties
```

## Property Value

This is a read only property whose value is a [PhysicalProperties](PhysicalProperties.md).

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version September 2015  

