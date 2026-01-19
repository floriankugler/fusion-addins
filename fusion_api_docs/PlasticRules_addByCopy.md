# PlasticRules.addByCopy Method

Parent Object: [PlasticRules](PlasticRules.md)  

## Description

Creates a new plastic rule by copying an existing rule. The new rule can then be edited to define the rule characteristics you want.

## Syntax

"plasticRules_var" is a variable referencing a [PlasticRules](PlasticRules.md) object.

```python
returnValue = plasticRules_var.addByCopy(existingPlasticRule, name)
```

## Return Value

| Type | Description |
|----|----|
| [PlasticRule](PlasticRule.md) | Returns the new PlasticRule object or will assert in the case where it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| existingPlasticRule | [PlasticRule](PlasticRule.md) | The existing PlasticRule object you want to copy. This can be a rule from the library or the design. |
| name | string | The name to assign to the new plastic rule. This name must be unique with respect to other plastic rules in the design or library it's created in. |

## Version

Introduced in version January 2024  

