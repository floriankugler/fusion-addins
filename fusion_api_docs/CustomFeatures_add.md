# CustomFeatures.add Method

Parent Object: [CustomFeatures](CustomFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new custom feature.

## Syntax

"customFeatures_var" is a variable referencing a [CustomFeatures](CustomFeatures.md) object.

```python
returnValue = customFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [CustomFeature](CustomFeature.md) | Returns the newly created CustomFeature. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CustomFeatureInput](CustomFeatureInput.md) | The CustomFeatureInput object that defines the information needed to create a custom feature. |

## Version

Introduced in version January 2021  

