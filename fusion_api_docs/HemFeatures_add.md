# HemFeatures.add Method

Parent Object: [HemFeatures](HemFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new Hem feature.

## Syntax

"hemFeatures_var" is a variable referencing a [HemFeatures](HemFeatures.md) object.

```python
returnValue = hemFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [HemFeature](HemFeature.md) | Returns the newly created HemFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [HemFeatureInput](HemFeatureInput.md) | A HemFeatureInput object that defines the desired hem. Use the createInput method to create a new HemFeatureInput object and then use methods on it (the HemFeatureInput object) to define the hem. |

## Version

Introduced in version September 2025  

