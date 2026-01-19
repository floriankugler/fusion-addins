# NCProgram.modifyUtility Method

Parent Object: [NCProgram](NCProgram.md)  

## Description

Get ModifyUtility for the current operation by given utility type.

## Syntax

"nCProgram_var" is a variable referencing a [NCProgram](NCProgram.md) object.

```python
returnValue = nCProgram_var.modifyUtility(utility)
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

Introduced in version September 2023  

