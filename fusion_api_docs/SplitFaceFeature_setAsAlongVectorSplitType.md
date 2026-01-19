# SplitFaceFeature.setAsAlongVectorSplitType Method

Parent Object: [SplitFaceFeature](SplitFaceFeature.md)  

## Description

Sets the split type to project the splitting tool along the direction defined by the specified entity.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitFaceFeature_var" is a variable referencing a [SplitFaceFeature](SplitFaceFeature.md) object.

```python
returnValue = splitFaceFeature_var.setAsAlongVectorSplitType(splittingTool, directionEntity)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true is setting the split type was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| splittingTool | [Base](Base.md) | Input entity(s) that defines the splitting tool. The splitting tool can be a single entity or an ObjectCollection containing faces or sketch curves. If faces are input, the edges of the face are used as the splitting tool. |
| directionEntity | [Base](Base.md) | An entity that defines the direction of projection of the splitting tool. This can be a linear BRepEdge, SketchLine, ConstructionLine, or a planar face where the face normal is used. |

## Version

Introduced in version May 2017  

