# PlasticRules.itemByName Method

Parent Object: [PlasticRules](PlasticRules.md)  

## Description

Function that returns the specified plastic rule using the name of the rule.

## Syntax

"plasticRules_var" is a variable referencing a [PlasticRules](PlasticRules.md) object.

```python
returnValue = plasticRules_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [PlasticRule](PlasticRule.md) | Returns the specified item or null if the specified name was not found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| name | string | The name of the rule within the collection to return. This is the name seen in the Plastic Rules dialog. |

## Version

Introduced in version January 2024  

