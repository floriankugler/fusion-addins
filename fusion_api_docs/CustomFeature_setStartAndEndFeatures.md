# CustomFeature.setStartAndEndFeatures Method

Parent Object: [CustomFeature](CustomFeature.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Sets the start and end features that will be grouped by the custom feature. The "features" in this case can be any object that is visible in the timeline, such as modeling features, sketches, and construction geometry. The input features and all features between them in the timeline will be grouped by the custom feature.  

The current start and end features can be determined by using the CustomFeature.features property and getting the first and last feature from the returned array.

## Syntax

"customFeature_var" is a variable referencing a [CustomFeature](CustomFeature.md) object.

```python
returnValue = customFeature_var.setStartAndEndFeatures(startFeature, endFeature)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if setting the start and end features was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| startFeature | [Base](Base.md) | The first feature in the timeline to be grouped by the custom feature. The start and the end features can be null which will result in moving all of the features out of the custom feature. This is useful in cases where you need to modify the inputs to a feature contained within a custom feature. You can move the features out of the custom feature, move the timeline marker as needed to edit the features, and then use this method again to add them back into the custom feature. |
| endFeature | [Base](Base.md) | The last feature in the timeline that will be grouped by the custom feature. This can be the same feature that is provided as the startFeature argument for the case where the custom feature contains a single feature. |

## Version

Introduced in version July 2021  

