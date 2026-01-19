# CAMAdditiveContainer.modifyUtility Method

Parent Object: [CAMAdditiveContainer](CAMAdditiveContainer.md)  

## Description

Get ModifyUtility for the current operation by given utility type.

## Syntax

"cAMAdditiveContainer_var" is a variable referencing a [CAMAdditiveContainer](CAMAdditiveContainer.md) object.

```python
returnValue = cAMAdditiveContainer_var.modifyUtility(utility)
```

## Return Value

| Type | Description |
|----|----|
| [ModifyUtility](ModifyUtility.md) | Returns ModifyUtility for specific type or null if the type is not compatible with the operation. |

## Parameters

| Name | Type | Description |
|----|----|----|
| utility | [ModifyUtilityTypes](ModifyUtilityTypes.md) | Defines the specific ModifyUtility. |

## Version

Introduced in version July 2024  

