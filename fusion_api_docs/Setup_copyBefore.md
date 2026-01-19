# Setup.copyBefore Method

Parent Object: [Setup](Setup.md)  

## Description

Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup.

## Syntax

"setup_var" is a variable referencing a [Setup](Setup.md) object.

```python
returnValue = setup_var.copyBefore(operation)
```

## Return Value

| Type    | Description                             |
|---------|-----------------------------------------|
| boolean | Returns if copy command was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| operation | [OperationBase](OperationBase.md) | Operation to copy targeted operation before. |

## Version

Introduced in version May 2024  

