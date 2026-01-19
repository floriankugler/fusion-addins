# BossFeature.createInput Method

Parent Object: [BossFeature](BossFeature.md)  

## Description

Creates object with inputs this feature represents. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"bossFeature_var" is a variable referencing a [BossFeature](BossFeature.md) object.

```python
returnValue = bossFeature_var.createInput()
```

## Return Value

| Type | Description |
|----|----|
| [BossFeatureInput](BossFeatureInput.md) | Returns BossFeatureInput this feature represent if successful. |

## Version

Introduced in version October 2022  

