# MergeFacesFeatureInput.inputFaces Property

Parent Object: [MergeFacesFeatureInput](MergeFacesFeatureInput.md)  

## Description

Gets and sets an array of BRepFace objects that define the faces the merge will be performed on. The faces need to be connected and from the same body (solid or surface).

## Syntax

"mergeFacesFeatureInput_var" is a variable referencing a MergeFacesFeatureInput object.  

```python
# Get the value of the property.
propertyValue = mergeFacesFeatureInput_var.inputFaces

# Set the value of the property.
mergeFacesFeatureInput_var.inputFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version September 2024  

