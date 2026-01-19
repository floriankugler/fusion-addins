# Operation.moveAfter Method

Parent Object: [Operation](Operation.md)  

## Description

Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup.

## Syntax

"operation_var" is a variable referencing an [Operation](Operation.md) object.

```python
returnValue = operation_var.moveAfter(operation)
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

Introduced in version May 2024  

