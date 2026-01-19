# SplitBodyFeature.setSplittingTool Method

Parent Object: [SplitBodyFeature](SplitBodyFeature.md)  

## Description

Sets the splitting tool used for the feature.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitBodyFeature_var" is a variable referencing a [SplitBodyFeature](SplitBodyFeature.md) object.

```python
returnValue = splitBodyFeature_var.setSplittingTool(splittingTool, isSplittingToolExtended)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| splittingTool | [Base](Base.md) | Input entity that defines the splitting tool. The splitting tool is a single entity that can be either a solid body, open body, construction plane, face, or sketch curve that partially or fully intersects the body to split. |
| isSplittingToolExtended | boolean | A boolean value for setting whether or not the splittingTool is to be automatically extended (if possible) so as to completely intersect the facesToSplit. |

## Version

Introduced in version June 2015  

