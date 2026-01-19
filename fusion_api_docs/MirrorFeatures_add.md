# MirrorFeatures.add Method

Parent Object: [MirrorFeatures](MirrorFeatures.md)  

## Description

Creates a new mirror feature.

## Syntax

"mirrorFeatures_var" is a variable referencing a [MirrorFeatures](MirrorFeatures.md) object.

```python
returnValue = mirrorFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [MirrorFeature](MirrorFeature.md) | Returns the newly created MirrorFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [MirrorFeatureInput](MirrorFeatureInput.md) | A MirrorFeatureInput object that defines the desired mirror. Use the createInput method to create a new MirrorFeatureInput object and then use methods on it (the MirrorFeatureInput object) to define the mirror. |

## Samples

| Name | Description |
|----|----|
| [mirrorFeatures.add](mirrorFeatures_add_Sample.md) | Demonstrates the mirrorFeatures.add method by mirroring the selected body around the base X-Y construction plane. |

## Version

Introduced in version November 2014  

