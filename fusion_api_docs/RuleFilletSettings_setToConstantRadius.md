# RuleFilletSettings.setToConstantRadius Method

Parent Object: [RuleFilletSettings](RuleFilletSettings.md)  

## Description

Changes the radius type to be constant.

## Syntax

"ruleFilletSettings_var" is a variable referencing a [RuleFilletSettings](RuleFilletSettings.md) object.

```python
returnValue = ruleFilletSettings_var.setToConstantRadius(radius)
```

## Parameters

| Name | Type | Description |
|----|----|----|
| radius | [ValueInput](ValueInput.md) | Input ValueInput object that defines the radius of the rule fillet. If the ValueInput uses a real value then it is interpreted as centimeters. If it is a string then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current document units for length. |

## Version

Introduced in version November 2025  

