# RuleFilletFeatureInput.facesOrFeatures Property

Parent Object: [RuleFilletFeatureInput](RuleFilletFeatureInput.md)  

## Description

Gets an array of BRepFace and/or Feature objects that are to have all their edges filleted. This is applicable only when ruleType is RuleFilletRuleTypes.AllEdgesRuleFilletRuleType. This is set by the setByAllEdges method.

## Syntax

"ruleFilletFeatureInput_var" is a variable referencing a RuleFilletFeatureInput object.  

```python
# Get the value of the property.
propertyValue = ruleFilletFeatureInput_var.facesOrFeatures
```

## Property Value

This is a read only property whose value is an array of type [Base](Base.md).

## Version

Introduced in version November 2025  

