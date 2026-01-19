# OperationBase.moveBefore Method

Parent Object: [OperationBase](OperationBase.md)  

## Description

Move operation in tree before the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup.

## Syntax

"operationBase_var" is a variable referencing an [OperationBase](OperationBase.md) object.

```python
returnValue = operationBase_var.moveBefore(operation)
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns if move operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operation | [OperationBase](OperationBase.md) | Operation to move targeted operation before. |

## Version

Introduced in version May 2024  

