# RuleFilletFeatureInput.setByAllEdges Method

Parent Object: [RuleFilletFeatureInput](RuleFilletFeatureInput.md)  

## Description

Method that adds an array of BRepFace and/or Feature objects to have all their edges to be filleted. Calling this method will set ruleType to RuleFilletRuleTypes.AllEdgesRuleFilletRuleType.

## Syntax

"ruleFilletFeatureInput_var" is a variable referencing a [RuleFilletFeatureInput](RuleFilletFeatureInput.md) object.

```python
returnValue = ruleFilletFeatureInput_var.setByAllEdges(facesOrFeatures)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| facesOrFeatures | Base\[\] | Input faces and/or features to have all their edges to be filleted. |

## Version

Introduced in version November 2025  

