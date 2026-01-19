# NCPrograms.itemByOperationId Method

Parent Object: [NCPrograms](NCPrograms.md)  

## Description

Returns the NC program with the specified operation id.

## Syntax

"nCPrograms_var" is a variable referencing a [NCPrograms](NCPrograms.md) object.

```python
returnValue = nCPrograms_var.itemByOperationId(id)
```

## Return Value

| Type | Description |
|----|----|
| [NCProgram](NCProgram.md) | Returns the specified NC program or null in the case where there is no NC program with the specified operation id. |

## Parameters

| Name | Type    | Description               |
|------|---------|---------------------------|
| id   | integer | The id of the NC program. |

## Version

Introduced in version April 2023  

