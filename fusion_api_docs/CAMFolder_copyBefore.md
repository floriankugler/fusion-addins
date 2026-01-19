# CAMFolder.copyBefore Method

Parent Object: [CAMFolder](CAMFolder.md)  

## Description

Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup.

## Syntax

"cAMFolder_var" is a variable referencing a [CAMFolder](CAMFolder.md) object.

```python
returnValue = cAMFolder_var.copyBefore(operation)
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

