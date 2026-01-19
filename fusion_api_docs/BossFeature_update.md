# BossFeature.update Method

Parent Object: [BossFeature](BossFeature.md)  

## Description

Changes the boss feature (or boss connection) to the input provided. To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"bossFeature_var" is a variable referencing a [BossFeature](BossFeature.md) object.

```python
returnValue = bossFeature_var.update(input)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [BossFeatureInput](BossFeatureInput.md) | The object defines inputs the feature will be set to. |

## Version

Introduced in version October 2022  

