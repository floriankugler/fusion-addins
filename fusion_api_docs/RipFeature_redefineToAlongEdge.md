# RipFeature.redefineToAlongEdge Method

Parent Object: [RipFeature](RipFeature.md)  

## Description

Redefines the feature to be a rip along an edge.

## Syntax

"ripFeature_var" is a variable referencing a [RipFeature](RipFeature.md) object.

```python
returnValue = ripFeature_var.redefineToAlongEdge(edge, gapDistance)
```

## Return Value

| Type    | Description                                       |
|---------|---------------------------------------------------|
| boolean | Returns true if the rip definition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edge | [BRepEdge](BRepEdge.md) | The BRepEdge that defines the rip. |
| gapDistance | [ValueInput](ValueInput.md) | The gap distance of the rip. |

## Version

Introduced in version September 2023  

