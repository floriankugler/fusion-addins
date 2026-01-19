# UserParameter.deleteMe Method

Parent Object: [UserParameter](UserParameter.md)  

## Description

Deletes the user parameter A parameter can only be deleted if it is a UserParameter and it is not referenced by other parameters.

## Syntax

"userParameter_var" is a variable referencing a [UserParameter](UserParameter.md) object.

```python
returnValue = userParameter_var.deleteMe()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns a bool indicating if the delete was successful or not. Bug!!! Currently returning true if the parameter can't be deleted because it is being referenced by other parameters. |

## Version

Introduced in version August 2014  

