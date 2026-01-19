# CAMHoleRecognition.modifyUtility Method

Parent Object: [CAMHoleRecognition](CAMHoleRecognition.md)  

## Description

Get ModifyUtility for the current operation by given utility type.

## Syntax

"cAMHoleRecognition_var" is a variable referencing a [CAMHoleRecognition](CAMHoleRecognition.md) object.

```python
returnValue = cAMHoleRecognition_var.modifyUtility(utility)
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

