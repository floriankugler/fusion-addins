# PlasticRuleValue.expression Property

Parent Object: [PlasticRuleValue](PlasticRuleValue.md)  

## Description

Gets and sets the expression of the plastic rule value. This can be an equation that includes the name "Thickness" and can also include length unit specifiers. For example, a valid expression is "Thickness / 2 + 1 mm". If no units are specified, the unit is implied and uses the units associated with the rule which can be mm or inch. For example an expression of "3" will be 3 inches if the rule units are inches or 3 mm if the rule units are millimeters. You can find out what units are used for a rule using the PlasticRule.units property.

## Syntax

"plasticRuleValue_var" is a variable referencing a PlasticRuleValue object.  

```python
# Get the value of the property.
propertyValue = plasticRuleValue_var.expression

# Set the value of the property.
plasticRuleValue_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2024  

