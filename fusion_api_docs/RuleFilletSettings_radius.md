# RuleFilletSettings.radius Property

Parent Object: [RuleFilletSettings](RuleFilletSettings.md)  

## Description

Gets the parameter controlling the radius of a constant radius rule fillet. This property will return null when isConstantRadius is false. To edit the radius, use properties on the parameter to change the value of the parameter.

## Syntax

"ruleFilletSettings_var" is a variable referencing a RuleFilletSettings object.  

```python
# Get the value of the property.
propertyValue = ruleFilletSettings_var.radius
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version November 2025  

