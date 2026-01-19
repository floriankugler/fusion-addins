# CAMHoleRecognition.copyBefore Method

Parent Object: [CAMHoleRecognition](CAMHoleRecognition.md)  

## Description

Creates a duplicate of the operation in the tree before the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup.

## Syntax

"cAMHoleRecognition_var" is a variable referencing a [CAMHoleRecognition](CAMHoleRecognition.md) object.

```python
returnValue = cAMHoleRecognition_var.copyBefore(operation)
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

