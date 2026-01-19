# SplitFaceFeature.setAsClosestPointSplitType Method

Parent Object: [SplitFaceFeature](SplitFaceFeature.md)  

## Description

Sets the split type to be a curve that defined by projecting the splitting curve to the closest point on the surface.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitFaceFeature_var" is a variable referencing a [SplitFaceFeature](SplitFaceFeature.md) object.

```python
returnValue = splitFaceFeature_var.setAsClosestPointSplitType(splittingTool)
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if setting the closest point split type was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| splittingTool | [Base](Base.md) | Input entity(s) that defines the splitting tool. The splitting tool can be a single entity or an ObjectCollection containing faces or sketch curves. If faces are input, the edges of the face are used as the splitting tool. |

## Version

Introduced in version May 2017  

