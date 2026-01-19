# CAMAdditiveContainer.moveAfter Method

Parent Object: [CAMAdditiveContainer](CAMAdditiveContainer.md)  

## Description

Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup.

## Syntax

"cAMAdditiveContainer_var" is a variable referencing a [CAMAdditiveContainer](CAMAdditiveContainer.md) object.

```python
returnValue = cAMAdditiveContainer_var.moveAfter(operation)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns if move operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operation | [OperationBase](OperationBase.md) | Operation to move targeted operation after. |

## Version

Introduced in version July 2024  

