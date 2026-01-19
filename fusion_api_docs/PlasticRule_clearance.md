# PlasticRule.clearance Property

Parent Object: [PlasticRule](PlasticRule.md)  

## Description

The clearance used for plastic features. When using a float to set the value, it is defined in centimeters. When using a string to set the expression, the units can be defined as part of the expression or it defaults to the units associated with the rule if no units are specified.

## Syntax

"plasticRule_var" is a variable referencing a PlasticRule object.  

```python
# Get the value of the property.
propertyValue = plasticRule_var.clearance
```

## Property Value

This is a read only property whose value is a [PlasticRuleValue](PlasticRuleValue.md).

## Version

Introduced in version January 2024  

