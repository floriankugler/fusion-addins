# EmbossFeatureInput.profiles Property

Parent Object: [EmbossFeatureInput](EmbossFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Gets and sets an array of Profile objects that define the shape of the emboss. The profile argument can be Profile and SketchText objects. When multiple objects are used, all profiles and sketch texts must be co-planar.

## Syntax

"embossFeatureInput_var" is a variable referencing an EmbossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = embossFeatureInput_var.profiles

# Set the value of the property.
embossFeatureInput_var.profiles = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [Base](Base.md).

## Version

Introduced in version September 2025  

