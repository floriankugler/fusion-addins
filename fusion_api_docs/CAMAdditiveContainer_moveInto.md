# CAMAdditiveContainer.moveInto Method

Parent Object: [CAMAdditiveContainer](CAMAdditiveContainer.md)  

## Description

Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup.

## Syntax

"cAMAdditiveContainer_var" is a variable referencing a [CAMAdditiveContainer](CAMAdditiveContainer.md) object.

```python
returnValue = cAMAdditiveContainer_var.moveInto(container)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns if move operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| container | [OperationBase](OperationBase.md) | Container to move targeted operation into. |

## Version

Introduced in version July 2024  

