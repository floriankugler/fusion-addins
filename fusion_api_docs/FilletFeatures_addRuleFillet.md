# FilletFeatures.addRuleFillet Method

Parent Object: [FilletFeatures](FilletFeatures.md)  

## Description

Creates a new rule fillet feature.

## Syntax

"filletFeatures_var" is a variable referencing a [FilletFeatures](FilletFeatures.md) object.

```python
returnValue = filletFeatures_var.addRuleFillet(input)
```

## Return Value

| Type | Description |
|----|----|
| [FilletFeature](FilletFeature.md) | Returns the newly created FilletFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [RuleFilletFeatureInput](RuleFilletFeatureInput.md) | A RuleFilletFeatureInput object that defines the desired fillet. Use the createRuleFilletInput method to create a new RuleFilletFeatureInput object and then use methods on it(the RuleFilletFeatureInput object) to define the fillet. |

## Version

Introduced in version November 2025  

