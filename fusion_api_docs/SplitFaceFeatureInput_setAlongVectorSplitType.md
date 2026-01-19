# SplitFaceFeatureInput.setAlongVectorSplitType Method

Parent Object: [SplitFaceFeatureInput](SplitFaceFeatureInput.md)  

## Description

Sets the split type to project the splitting tool along the direction defined by the specified entity.

## Syntax

"splitFaceFeatureInput_var" is a variable referencing a [SplitFaceFeatureInput](SplitFaceFeatureInput.md) object.

```python
returnValue = splitFaceFeatureInput_var.setAlongVectorSplitType(directionEntity)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true is setting the split type was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| directionEntity | [Base](Base.md) | An entity that defines the direction of projection of the splitting tool. This can be a linear BRepEdge, SketchLine, ConstructionLine, or a planar face where the face normal is used. |

## Samples

| Name | Description |
|----|----|
| [Split Face Feature API Sample](SplitFaceFeatureSample_Sample.md) | Demonstrates creating a new split face feature. |

## Version

Introduced in version May 2017  

