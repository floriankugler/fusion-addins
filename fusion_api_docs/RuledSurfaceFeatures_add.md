# RuledSurfaceFeatures.add Method

Parent Object: [RuledSurfaceFeatures](RuledSurfaceFeatures.md)  

## Description

Creates a new RuledSurface feature.

## Syntax

"ruledSurfaceFeatures_var" is a variable referencing a [RuledSurfaceFeatures](RuledSurfaceFeatures.md) object.

```python
returnValue = ruledSurfaceFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [RuledSurfaceFeature](RuledSurfaceFeature.md) | Returns the newly created RuledSurfaceFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [RuledSurfaceFeatureInput](RuledSurfaceFeatureInput.md) | An RuledSurfaceFeatureInput object that defines the desired RuledSurface feature. Use the createInput method to create a new RuledSurfaceFeatureInput object and then use methods on it (the RuledSurfaceFeatureInput object) to define the desired options for the ruled surface feature. |

## Version

Introduced in version September 2020  

