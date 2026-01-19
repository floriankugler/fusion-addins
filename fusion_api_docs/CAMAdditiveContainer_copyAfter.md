# CAMAdditiveContainer.copyAfter Method

Parent Object: [CAMAdditiveContainer](CAMAdditiveContainer.md)  

## Description

Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup.

## Syntax

"cAMAdditiveContainer_var" is a variable referencing a [CAMAdditiveContainer](CAMAdditiveContainer.md) object.

```python
returnValue = cAMAdditiveContainer_var.copyAfter(operation)
```

## Return Value

| Type    | Description                             |
|---------|-----------------------------------------|
| boolean | Returns if copy command was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operation | [OperationBase](OperationBase.md) | Operation to copy targeted operation after. |

## Version

Introduced in version July 2024  

