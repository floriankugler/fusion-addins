# Operation.copyInto Method

Parent Object: [Operation](Operation.md)  

## Description

Creates a duplicate of the operation into the given container. You can only copy into containers, such as setups or folders. Copied operation will be copied at the end of all operations already in the container. Throws an exception if a not allowed copy operation is made for example copying a setup into a setup.

## Syntax

"operation_var" is a variable referencing an [Operation](Operation.md) object.

```python
returnValue = operation_var.copyInto(container)
```

## Return Value

| Type    | Description                             |
|---------|-----------------------------------------|
| boolean | Returns if copy command was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| container | [OperationBase](OperationBase.md) | Container to copy targeted operation into. |

## Version

Introduced in version May 2024  

