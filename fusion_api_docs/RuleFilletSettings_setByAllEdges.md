# RuleFilletSettings.setByAllEdges Method

Parent Object: [RuleFilletSettings](RuleFilletSettings.md)  

## Description

Method that adds an array of BRepFace and/or Feature objects to have all their edges filleted. Calling this method will set ruleType to RuleFilletRuleTypes.AllEdgesRuleFilletRuleType.

## Syntax

"ruleFilletSettings_var" is a variable referencing a [RuleFilletSettings](RuleFilletSettings.md) object.

```python
returnValue = ruleFilletSettings_var.setByAllEdges(facesOrFeatures)
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

