# RipFeatureInput.setAlongEdge Method

Parent Object: [RipFeatureInput](RipFeatureInput.md)  

## Description

Specifies the rip feature will be along an edge.

## Syntax

"ripFeatureInput_var" is a variable referencing a [RipFeatureInput](RipFeatureInput.md) object.

```python
returnValue = ripFeatureInput_var.setAlongEdge(edge, gapDistance)
```

## Return Value

| Type    | Description                                         |
|---------|-----------------------------------------------------|
| boolean | Returns true if the defining the rip is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| edge | [BRepEdge](BRepEdge.md) | The BRepEdge that defines the location of the rip. |
| gapDistance | [ValueInput](ValueInput.md) | The gap distance of the rip. |

## Version

Introduced in version September 2023  

