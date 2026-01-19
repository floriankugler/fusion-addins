# CAMFolder.moveInto Method

Parent Object: [CAMFolder](CAMFolder.md)  

## Description

Move operation in tree into the given container. This only works with setups, patterns and folders. Moved operation will be moved at the end of all operations already in the container. Throws an exception if a not allowed move is made for example moving a setup into a setup.

## Syntax

"cAMFolder_var" is a variable referencing a [CAMFolder](CAMFolder.md) object.

```python
returnValue = cAMFolder_var.moveInto(container)
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

