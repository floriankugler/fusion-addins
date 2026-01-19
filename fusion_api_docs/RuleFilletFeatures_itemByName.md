# RuleFilletFeatures.itemByName Method

Parent Object: [RuleFilletFeatures](RuleFilletFeatures.md)  

## Description

Function that returns the specified rule fillet feature using the name of the feature.

## Syntax

"ruleFilletFeatures_var" is a variable referencing a [RuleFilletFeatures](RuleFilletFeatures.md) object.

```python
returnValue = ruleFilletFeatures_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [RuleFilletFeature](RuleFilletFeature.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the feature within the collection to return. This is the name seen in the timeline. |

## Version

Introduced in version September 2015  

