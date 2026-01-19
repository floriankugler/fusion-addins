# Operation.copyAfter Method

Parent Object: [Operation](Operation.md)  

## Description

Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup.

## Syntax

"operation_var" is a variable referencing an [Operation](Operation.md) object.

```python
returnValue = operation_var.copyAfter(operation)
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

Introduced in version May 2024  

