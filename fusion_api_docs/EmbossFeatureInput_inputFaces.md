# EmbossFeatureInput.inputFaces Property

Parent Object: [EmbossFeatureInput](EmbossFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets an array of BRepFace objects that define the faces the emboss will be performed on. By default, faces that are tangent to any of the input faces are also used. Use the isTangentChain property of the EmbossFeatureInput object to disable the use of tangent faces. If multiple inputFaces are provided, they must all be on the same body.

## Syntax

"embossFeatureInput_var" is a variable referencing an EmbossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = embossFeatureInput_var.inputFaces

# Set the value of the property.
embossFeatureInput_var.inputFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [BRepFace](BRepFace.md).

## Version

Introduced in version September 2025  

