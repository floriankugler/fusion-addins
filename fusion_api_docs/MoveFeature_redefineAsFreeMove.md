# MoveFeature.redefineAsFreeMove Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Redefines the move feature to be described by an arbitrary translation and orientation which is defined using a transformation matrix.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.redefineAsFreeMove(transform)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if the re-definition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| transform | [Matrix3D](Matrix3D.md) | The transformation matrix that defines the transform to apply. The matrix must be an orthogonal matrix; that is the axes are perpendicular to each other and there isn't any scaling or mirroring defined. |

## Version

Introduced in version January 2023  

