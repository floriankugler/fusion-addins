# CAMPattern.copyAfter Method

Parent Object: [CAMPattern](CAMPattern.md)  

## Description

Creates a duplicate of the operation in the tree after the given operation. Throws an exception if a not allowed copy operation is made for example copying a operation out of a setup.

## Syntax

"cAMPattern_var" is a variable referencing a [CAMPattern](CAMPattern.md) object.

```python
returnValue = cAMPattern_var.copyAfter(operation)
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

