# DocumentToolLibrary.operationsByTool Method

Parent Object: [DocumentToolLibrary](DocumentToolLibrary.md)  

## Description

Returns all operations that use the given tool. The tool must exist in the document tool library. Raises an error if the tool is not in the document.

## Syntax

"documentToolLibrary_var" is a variable referencing a [DocumentToolLibrary](DocumentToolLibrary.md) object.

```python
returnValue = documentToolLibrary_var.operationsByTool(tool)
```

## Return Value

| Type                           | Description                               |
|--------------------------------|-------------------------------------------|
| [Operation](Operation.md)\[\] | Returns operations using a specific tool. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tool | [Tool](Tool.md) | The tool to search for in operations. The tool must exist in the document. |

## Version

Introduced in version April 2023  

