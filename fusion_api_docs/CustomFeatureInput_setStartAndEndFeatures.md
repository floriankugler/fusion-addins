# CustomFeatureInput.setStartAndEndFeatures Method

Parent Object: [CustomFeatureInput](CustomFeatureInput.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Sets the start and end features that the custom feature will group. A "feature" in this case is an object that is visible in the timeline, such as modeling features, sketches, and construction geometry. The custom feature will group the input start and end features and all features between them in the timeline.  

You can determine the current start and end features using the features property and use the first and last features returned. If the custom feature contains a single feature, you can use the same feature for both the start and end feature arguments. You can also use null for both arguments to remove all features from a custom feature. The custom feature still exists but will be empty, and the features will be displayed individually within the timeline.

## Syntax

"customFeatureInput_var" is a variable referencing a [CustomFeatureInput](CustomFeatureInput.md) object.

```python
returnValue = customFeatureInput_var.setStartAndEndFeatures(startFeature, endFeature)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if setting the start and end features was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startFeature | [Base](Base.md) | The first feature in the timeline that the custom feature will group. |
| endFeature | [Base](Base.md) | The last feature in the timeline that the custom feature will group. When creating a custom feature that contains a single feature, this can be the same feature as the startFeature argument. |

## Version

Introduced in version August 2021  

