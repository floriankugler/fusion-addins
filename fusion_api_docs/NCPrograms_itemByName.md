# NCPrograms.itemByName Method

Parent Object: [NCPrograms](NCPrograms.md)  

## Description

Returns the NC program with the specified name.

## Syntax

"nCPrograms_var" is a variable referencing a [NCPrograms](NCPrograms.md) object.

```python
returnValue = nCPrograms_var.itemByName(name)
```

## Return Value

| Type | Description |
|----|----|
| [NCProgram](NCProgram.md) | Returns the specified NC program or null in the case where there is no NC program with the specified name. If there are multiple NC programs with the same name, the first item in the tree will be returned. |

## Parameters

| Name | Type   | Description                                               |
|------|--------|-----------------------------------------------------------|
| name | string | The name (as it appears in the browser) of the operation. |

## Version

Introduced in version April 2023  

