# MoveFeature.redefineAsPointToPoint Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Redefines the move feature to be a translation from one point to another.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.redefineAsPointToPoint(originPoint, targetPoint)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the redefinition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| originPoint | [Base](Base.md) | The first point that defines the start position of the move. |
| targetPoint | [Base](Base.md) | The second point that defines the direction and distance of the move. |

## Version

Introduced in version January 2023  

