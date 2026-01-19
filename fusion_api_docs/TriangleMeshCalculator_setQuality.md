# TriangleMeshCalculator.setQuality Method

Parent Object: [TriangleMeshCalculator](TriangleMeshCalculator.md)  

## Description

This is a simplified way to set the various settings that control the resulting mesh. When used it automatically adjusts all of the property values appropriately. It does this for the given geometry by computing its bounding box diameter. Then the surface tolerance is calculated as shown below where the meshLOD is the "Level of Detail" and is described in more detail below. The diameter is the bounding box diameter.  

double nodeApproximateSize = std::pow(2.0, meshLOD); double fracTol = 1.0 / nodeApproximateSize; surfaceTolerance = fracTol \* diameter;

## Syntax

"triangleMeshCalculator_var" is a variable referencing a [TriangleMeshCalculator](TriangleMeshCalculator.md) object.

```python
returnValue = triangleMeshCalculator_var.setQuality(triangleMeshQuality)
```

## Return Value

| Type    | Description                                         |
|---------|-----------------------------------------------------|
| boolean | Returns true if setting the quality was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| triangleMeshQuality | [TriangleMeshQualityOptions](TriangleMeshQualityOptions.md) | The mesh quality is specified by using an item from the enum list where the following items result in a corresponding mesh LOD that's used in the equation above. LowQualityTriangleMesh: 8 NormalQualityTriangleMesh: 11 HighQualityTriangleMesh: 13 VeryHighQualityTriangleMesh: 15 |

## Version

Introduced in version August 2014  

