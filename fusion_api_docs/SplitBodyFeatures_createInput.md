# SplitBodyFeatures.createInput Method

Parent Object: [SplitBodyFeatures](SplitBodyFeatures.md)  

## Description

Creates a SplitBodyFeatureInput object. Use properties and methods on this object to define the split body you want to create and then use the Add method, passing in the SplitBodyFeatureInput object.

## Syntax

"splitBodyFeatures_var" is a variable referencing a [SplitBodyFeatures](SplitBodyFeatures.md) object.

```python
returnValue = splitBodyFeatures_var.createInput(splitBodies, splittingTool, isSplittingToolExtended)
```

## Return Value

| Type | Description |
|----|----|
| [SplitBodyFeatureInput](SplitBodyFeatureInput.md) | Returns the newly created SplitBodyFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| splitBodies | [Base](Base.md) | Input solid body or open bodies to be split. This can be a single BRepBody or an ObjectCollection if multiple bodies are to be split. |
| splittingTool | [Base](Base.md) | Input entity that defines the splitting tool. The splitting tool is a single entity that can be either a solid or open BRepBody, construction plane, profile, or a face. |
| isSplittingToolExtended | boolean | A boolean value for setting whether or not the splitting tool is to be automatically extended (if possible) so as to completely intersect the bodyToSplit. |

## Samples

| Name | Description |
|----|----|
| [splitBodyFeatures.add](splitBodyfeatures_add_Sample.md) | Demonstrates the splitBodyFeatures.add method. |
| [Split Body Feature API Sample](SplitBodyFeatureSample_Sample.md) | Demonstrates creating a new split body feature. |

## Version

Introduced in version June 2015  

