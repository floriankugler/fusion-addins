# EmbossFeatureInput.creationOccurrence Property

Parent Object: [EmbossFeatureInput](EmbossFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

In order for geometry to be transformed correctly, an Occurrence for creation needs to be specified when the emboss feature is created based on geometry (e.g. a profile and/or face(s)) in another component AND (the emboss feature) is not in the root component. The creationOccurrence is analogous to the active occurrence in the UI

## Syntax

"embossFeatureInput_var" is a variable referencing an EmbossFeatureInput object.  

```python
# Get the value of the property.
propertyValue = embossFeatureInput_var.creationOccurrence

# Set the value of the property.
embossFeatureInput_var.creationOccurrence = propertyValue
```

## Property Value

This is a read/write property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version September 2025  

