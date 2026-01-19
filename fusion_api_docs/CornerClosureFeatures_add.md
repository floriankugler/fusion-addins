# CornerClosureFeatures.add Method

Parent Object: [CornerClosureFeatures](CornerClosureFeatures.md)

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

Creates a new Corner Closure feature.

## Syntax

"cornerClosureFeatures_var" is a variable referencing a [CornerClosureFeatures](CornerClosureFeatures.md) object.

```python
returnValue = cornerClosureFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [CornerClosureFeature](CornerClosureFeature.md) | Returns the newly created CornerClosureFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CornerClosureFeatureInput](CornerClosureFeatureInput.md) | A CornerClosureFeatureInput object that defines the desired corner closure. Use the createCornerClosureFeatureInput method to create a new CornerClosureFeatureInput object and then use methods on it (the CornerClosureFeatureInput object) to define the corner closure. |

## Version

Introduced in version January 2026  

