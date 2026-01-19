# PlasticRule.deleteMe Method

Parent Object: [PlasticRule](PlasticRule.md)  

## Description

Deletes the rule from the design or library. If the rule is in the library and set as the default rule, you cannot delete it. If the rule is in a design and is used by a component you cannot delete it.

## Syntax

"plasticRule_var" is a variable referencing a [PlasticRule](PlasticRule.md) object.

```python
returnValue = plasticRule_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version January 2024  

