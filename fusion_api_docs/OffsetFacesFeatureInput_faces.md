# OffsetFacesFeatureInput.faces Property

Parent Object: [OffsetFacesFeatureInput](OffsetFacesFeatureInput.md)  

## Description

An array of BRepFace objects you want to offset. These faces can exist on multiple bodies and in multiple components. They cannot be in an externally referenced component.

## Syntax

"offsetFacesFeatureInput_var" is a variable referencing an OffsetFacesFeatureInput object.  

```python
# Get the value of the property.
propertyValue = offsetFacesFeatureInput_var.faces

# Set the value of the property.
offsetFacesFeatureInput_var.faces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version November 2025  

