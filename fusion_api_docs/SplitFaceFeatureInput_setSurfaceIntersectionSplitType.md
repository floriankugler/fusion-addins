# SplitFaceFeatureInput.setSurfaceIntersectionSplitType Method

Parent Object: [SplitFaceFeatureInput](SplitFaceFeatureInput.md)  

## Description

Set the split type to be a surface to surface intersection. If the split tool is a curve it will be extruded into a surface to use in the split. If it's a surface, the surface will be used and optionally extended to fully intersect the faces to be split.

## Syntax

"splitFaceFeatureInput_var" is a variable referencing a [SplitFaceFeatureInput](SplitFaceFeatureInput.md) object.

```python
returnValue = splitFaceFeatureInput_var.setSurfaceIntersectionSplitType(isSplittingToolExtended)
```

## Return Value

| Type    | Description                                            |
|---------|--------------------------------------------------------|
| boolean | Returns true is setting the split type was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| isSplittingToolExtended | boolean | Specifies if the splitting tool should be extended so that is fully intersects the faces to be split. |

## Version

Introduced in version May 2017  

