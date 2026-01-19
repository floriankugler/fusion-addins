# RipFeature.redefineToBetweenPoints Method

Parent Object: [RipFeature](RipFeature.md)  

## Description

Redefines the feature to be a rip between two points.

## Syntax

"ripFeature_var" is a variable referencing a [RipFeature](RipFeature.md) object.

```python
# Uses no optional arguments.
returnValue = ripFeature_var.redefineToBetweenPoints(pointOneEntity, pointTwoEntity, gapDistance)

# Uses optional arguments.
returnValue = ripFeature_var.redefineToBetweenPoints(pointOneEntity, pointTwoEntity, gapDistance, pointOneOffset, pointTwoOffset)
```

## Return Value

| Type    | Description                                       |
|---------|---------------------------------------------------|
| boolean | Returns true if the rip definition is successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| pointOneEntity | [Base](Base.md) | The first point of the rip. This can be defined using a BrepVertex or a BRepEdge and offset to define where the point is along the edge. If an edge is specified, the pointOneOffset parameter must be specified. |
| pointTwoEntity | [Base](Base.md) | The second point of the rip and must lie on the same face as point 1. This can be defined using a BrepVertex or a BRepEdge and an offset to define where the point is along the edge. If an edge is specified, the pointTwoOffset parameter must be specified. |
| gapDistance | [ValueInput](ValueInput.md) | The gap distance of the rip. |
| pointOneOffset | [ValueInput](ValueInput.md) | If the first point lies on an edge, then this is the offset along the edge which defines the point. This is the physical distance from the topological start of the edge. If the offset is negative or exceeds the edge length, the corresponding vertex of the edge will be used. This is an optional argument whose default value is null. |
| pointTwoOffset | [ValueInput](ValueInput.md) | If the second point lies on an edge, then this is the offset along the edge which defines the point. This is the physical distance from the topological start of the edge. If the offset is negative or exceeds the edge length, the corresponding vertex of the edge will be used. This is an optional argument whose default value is null. |

## Version

Introduced in version September 2023  

