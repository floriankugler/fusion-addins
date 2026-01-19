# RuleFilletFeatureInput.setByBetweenFacesOrFeatures Method

Parent Object: [RuleFilletFeatureInput](RuleFilletFeatureInput.md)  

## Description

Method that adds two sets of BRepFace and/or Feature objects to have the edges between them filleted. Call this method will set ruleType to RuleFilletRuleTypes.BetweenFacesOrFeaturesRuleFilletRuleType.

## Syntax

"ruleFilletFeatureInput_var" is a variable referencing a [RuleFilletFeatureInput](RuleFilletFeatureInput.md) object.

```python
returnValue = ruleFilletFeatureInput_var.setByBetweenFacesOrFeatures(facesOrFeaturesOne, facesOrFeaturesTwo)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| facesOrFeaturesOne | Base\[\] | Input first array of BRepFace and/or Feature objects. |
| facesOrFeaturesTwo | Base\[\] | Input second array of BRepFace and/or Feature objects. |

## Version

Introduced in version November 2025  

