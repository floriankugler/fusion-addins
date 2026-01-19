# FaceGroup.tempId Property

Parent Object: [FaceGroup](FaceGroup.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Returns the temporary ID of this face group. This ID is only good while the document remains open and as long as the owning mesh body is not modified in any way.

## Syntax

"faceGroup_var" is a variable referencing a FaceGroup object.  

```python
# Get the value of the property.
propertyValue = faceGroup_var.tempId
```

## Property Value

This is a read only property whose value is an integer.

## Version

Introduced in version September 2024  

