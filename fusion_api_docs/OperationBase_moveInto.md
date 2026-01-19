# OperationBase.moveInto Method

Parent Object: [OperationBase](OperationBase.md)  

## Description

Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup.

## Syntax

"operationBase_var" is a variable referencing an [OperationBase](OperationBase.md) object.

```python
returnValue = operationBase_var.moveInto(container)
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

Introduced in version May 2024  

