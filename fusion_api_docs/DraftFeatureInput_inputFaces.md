# DraftFeatureInput.inputFaces Property

Parent Object: [DraftFeatureInput](DraftFeatureInput.md)  

## Description

Gets and sets the input faces. If IsTangentChain is true, all the faces that are tangentially connected to the input faces (if any) will also be included.

## Syntax

"draftFeatureInput_var" is a variable referencing a DraftFeatureInput object.  

```python
# Get the value of the property.
propertyValue = draftFeatureInput_var.inputFaces

# Set the value of the property.
draftFeatureInput_var.inputFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version January 2015  

