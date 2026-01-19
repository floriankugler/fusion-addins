# EmbossFeatures.add Method

Parent Object: [EmbossFeatures](EmbossFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new emboss feature.

## Syntax

"embossFeatures_var" is a variable referencing an [EmbossFeatures](EmbossFeatures.md) object.

```python
returnValue = embossFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [EmbossFeature](EmbossFeature.md) | Returns the newly created EmbossFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [EmbossFeatureInput](EmbossFeatureInput.md) | An EmbossFeatureInput object that defines the desired emboss feature. Use the createInput method to create a new EmbossFeatureInput object and then use methods on the EmbossFeatureInput object to define the emboss feature. |

## Version

Introduced in version September 2025  

