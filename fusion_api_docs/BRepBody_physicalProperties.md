# BRepBody.physicalProperties Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc of this body. Property values will be calculated using the 'LowCalculationAccuracy' setting when using this property to get the PhysicalProperties object. To specify a higher calculation tolerance, use the getPhysicalProperties method on the Design class instead.

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.physicalProperties
```

## Property Value

This is a read only property whose value is a [PhysicalProperties](PhysicalProperties.md).

## Samples

| Name | Description |
|----|----|
| [Get Physical Properties API Sample](GetPhysicalProperties_Sample.md) | Script that demonstrates getting physical properties using the API. When this script is run it will create a new document, build a simple model, and get the various physical properties from the model. |

## Version

Introduced in version September 2015  

