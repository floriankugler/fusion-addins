# OffsetFacesFeature.inputFaces Property

Parent Object: [OffsetFacesFeature](OffsetFacesFeature.md)  

## Description

Returns an array of BRepFace objects that were offset. The timeline must be rolled back to immediately before this feature when getting or setting this property so the faces are available.

## Syntax

"offsetFacesFeature_var" is a variable referencing an OffsetFacesFeature object.  

```python
# Get the value of the property.
propertyValue = offsetFacesFeature_var.inputFaces

# Set the value of the property.
offsetFacesFeature_var.inputFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version November 2025  

