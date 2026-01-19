# HoleFeatureInput.setPositionBySketchPoints Method

Parent Object: [HoleFeatureInput](HoleFeatureInput.md)  

## Description

Defines the position and orientation of the hole using a set of sketch points.

## Syntax

"holeFeatureInput_var" is a variable referencing a [HoleFeatureInput](HoleFeatureInput.md) object.

```python
returnValue = holeFeatureInput_var.setPositionBySketchPoints(sketchPoints)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchPoints | [ObjectCollection](ObjectCollection.md) | A collection of sketch points that defines the positions of the holes. The orientation is inferred from the normal of the point's parent sketch. The natural direction will be opposite the normal of the sketch. The points can be from multiple sketches but they must all be co-planar. |

## Samples

| Name | Description |
|----|----|
| [Hole Feature API Sample](HoleFeatureSample_Sample.md) | Demonstrates creating a new hole feature. |

## Version

Introduced in version June 2015  

