# RuleFilletFeatureInput.setAsymmetricOffsets Method

Parent Object: [RuleFilletFeatureInput](RuleFilletFeatureInput.md)  

## Description

Sets the fillet to be an asymmetric fillet and defines the two offsets.

## Syntax

"ruleFilletFeatureInput_var" is a variable referencing a [RuleFilletFeatureInput](RuleFilletFeatureInput.md) object.

```python
returnValue = ruleFilletFeatureInput_var.setAsymmetricOffsets(offsetOne, offsetTwo)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| offsetOne | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset distance of the fillet in the first direction. If the ValueInput uses a real then it is interpreted as centimeters. If it is a string, then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |
| offsetTwo | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset distance of the fillet in the second direction. If the ValueInput uses a real, then it is interpreted as centimeters. If it is a string, then the units can be defined as part of the string (i.e. "2 in") or if no units are specified it is interpreted using the current default units for length. |

## Version

Introduced in version November 2025  

