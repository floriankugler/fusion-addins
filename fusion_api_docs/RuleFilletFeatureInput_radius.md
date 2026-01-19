# RuleFilletFeatureInput.radius Property

Parent Object: [RuleFilletFeatureInput](RuleFilletFeatureInput.md)  

## Description

Gets and sets the radius of the fillet. Setting this will set the fillet to a constant radius fillet and any asymmetric information will be lost. Returns null in the case the fillet is asymmetric.

## Syntax

"ruleFilletFeatureInput_var" is a variable referencing a RuleFilletFeatureInput object.  

```python
# Get the value of the property.
propertyValue = ruleFilletFeatureInput_var.radius

# Set the value of the property.
ruleFilletFeatureInput_var.radius = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version November 2025  

