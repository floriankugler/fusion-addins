# ModelParameter.deleteMe Method

Parent Object: [ModelParameter](ModelParameter.md)  

## Description

Deletes this ModelParameter. As a general rule, model parameters cannot be deleted because features depend on them. However, there are uncommon workflows where a parameter no longer has any dependents and is not automatically deleted. You can use the isDeletable property to see if the parameter is in this state and can successfully be deleted.

## Syntax

"modelParameter_var" is a variable referencing a [ModelParameter](ModelParameter.md) object.

```python
returnValue = modelParameter_var.deleteMe()
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Version

Introduced in version May 2025  

