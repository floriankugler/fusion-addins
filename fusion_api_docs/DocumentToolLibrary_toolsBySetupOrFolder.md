# DocumentToolLibrary.toolsBySetupOrFolder Method

Parent Object: [DocumentToolLibrary](DocumentToolLibrary.md)  

## Description

Returns all tools used in a given setup or folder. Given setup or folder must belong to the document of the DocumentToolLibrary. Raises an error if given operation is not in the document.

## Syntax

"documentToolLibrary_var" is a variable referencing a [DocumentToolLibrary](DocumentToolLibrary.md) object.

```python
returnValue = documentToolLibrary_var.toolsBySetupOrFolder(setupOrFolder)
```

## Return Value

| Type                 | Description                                       |
|----------------------|---------------------------------------------------|
| [Tool](Tool.md)\[\] | Returns tools used by a specific setup or folder. |

## Parameters

| Name | Type | Description |
|----|----|----|
| setupOrFolder | [OperationBase](OperationBase.md) | The setup or folder to get tools from. Must belong to the document. |

## Version

Introduced in version July 2023  

