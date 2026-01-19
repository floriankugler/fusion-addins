# CAMFolder.moveBefore Method

Parent Object: [CAMFolder](CAMFolder.md)  

## Description

Move operation in tree before the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup.

## Syntax

"cAMFolder_var" is a variable referencing a [CAMFolder](CAMFolder.md) object.

```python
returnValue = cAMFolder_var.moveBefore(operation)
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

