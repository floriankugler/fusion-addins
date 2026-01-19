# ExtrudeFeatureInput.startExtent Property

Parent Object: [ExtrudeFeatureInput](ExtrudeFeatureInput.md)  

## Description

Gets and sets the extent used to define the start of the extrusion. When a new ExtrudeFeatureInput object is created the start extent is initialized to be the profile plane but you can change it to a profile plane with offset or from an object by setting this property with either a OffsetStartDefinition or an EntityStartDefinition object. You can get either one of those objects by using the static create method on the class.

## Syntax

"extrudeFeatureInput_var" is a variable referencing an ExtrudeFeatureInput object.  

```python
# Get the value of the property.
propertyValue = extrudeFeatureInput_var.startExtent

# Set the value of the property.
extrudeFeatureInput_var.startExtent = propertyValue
```

## Property Value

This is a read/write property whose value is an [ExtentDefinition](ExtentDefinition.md).

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |

## Version

Introduced in version November 2016  

