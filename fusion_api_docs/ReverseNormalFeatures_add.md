# ReverseNormalFeatures.add Method

Parent Object: [ReverseNormalFeatures](ReverseNormalFeatures.md)  

## Description

Creates a new Reverse Normal feature.

## Syntax

"reverseNormalFeatures_var" is a variable referencing a [ReverseNormalFeatures](ReverseNormalFeatures.md) object.

```python
returnValue = reverseNormalFeatures_var.add(surfaces)
```

## Return Value

| Type | Description |
|----|----|
| [ReverseNormalFeature](ReverseNormalFeature.md) | Returns the newly created ReverseNormalFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| surfaces | [ObjectCollection](ObjectCollection.md) | One or more surface bodies (open BRepBodies) containing the faces whose normals are to be reversed. All faces of the input surface bodies get reversed. |

## Samples

| Name | Description |
|----|----|
| [reverseNormalFeatures.add](reverseNormalFeatures_add_Sample.md) | Demonstrates the reverseNormalFeatures.add method. |
| [Reverse Normal Feature](ReverseNormalFeatureSample_Sample.md) | Demonstrates creating a new reverse normal feature. |

## Version

Introduced in version November 2015  

