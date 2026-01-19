# PlasticRules.item Method

Parent Object: [PlasticRules](PlasticRules.md)  

## Description

Function that returns the specified plastic rule using an index into the collection.

## Syntax

"plasticRules_var" is a variable referencing a [PlasticRules](PlasticRules.md) object.

```python
returnValue = plasticRules_var.item(index)
```

## Return Value

| Type | Description |
|----|----|
| [PlasticRule](PlasticRule.md) | Returns the specified item or null if an invalid index was specified. |

## Parameters

| Name | Type | Description |
|----|----|----|
| index | uinteger | The index of the item within the collection to return. The first item in the collection has an index of 0. |

## Version

Introduced in version January 2024  

