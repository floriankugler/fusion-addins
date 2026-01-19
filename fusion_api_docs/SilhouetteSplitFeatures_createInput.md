# SilhouetteSplitFeatures.createInput Method

Parent Object: [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md)  

## Description

Creates a SilhouetteSplitFeatureInput object. Use properties and methods on this object to define the silhouette split you want to create and then use the Add method, passing in the SilhouetteSplitFeatureInput object.

## Syntax

"silhouetteSplitFeatures_var" is a variable referencing a [SilhouetteSplitFeatures](SilhouetteSplitFeatures.md) object.

```python
returnValue = silhouetteSplitFeatures_var.createInput(viewDirection, targetBody, operation)
```

## Return Value

| Type | Description |
|----|----|
| [SilhouetteSplitFeatureInput](SilhouetteSplitFeatureInput.md) | Returns the newly created SilhouetteSplitFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| viewDirection | [Base](Base.md) | A construction axis, linear BRepEdge, planar BRepFace or a construction plane that defines the view direction where the silhouette is calculated. |
| targetBody | [BRepBody](BRepBody.md) | Input the single solid body to split |
| operation | [SilhouetteSplitOperations](SilhouetteSplitOperations.md) | The type of silhouette split operation to perform. |

## Samples

| Name | Description |
|----|----|
| [silhouetteSplitFeatures.add](silhouetteSplitFeatures_add_Sample.md) | Demonstrates the silhouetteSplitFeatures.add method. The Silhouette Split feature is limited in the bodies it will split. The simplest body to get a valid result is to create a sphere and split it. |
| [Silhouette Split Feature API Sample](SilhouetteSplitFeatureSample_Sample.md) | Demonstrates creating a new silhouette split feature. |

## Version

Introduced in version June 2015  

