# CAMHoleRecognition.moveAfter Method

Parent Object: [CAMHoleRecognition](CAMHoleRecognition.md)  

## Description

Move operation in tree after the given operation. Throws an exception if a not allowed move is made for example moving a operation out of a setup.

## Syntax

"cAMHoleRecognition_var" is a variable referencing a [CAMHoleRecognition](CAMHoleRecognition.md) object.

```python
returnValue = cAMHoleRecognition_var.moveAfter(operation)
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

