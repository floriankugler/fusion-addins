# SelectionCommandInput.selection Method

Parent Object: [SelectionCommandInput](SelectionCommandInput.md)  

## Description

Returns the selection at the specified index.

## Syntax

"selectionCommandInput_var" is a variable referencing a [SelectionCommandInput](SelectionCommandInput.md) object.

```python
returnValue = selectionCommandInput_var.selection(index)
```

## Return Value

| Type | Description |
|----|----|
| [Selection](Selection.md) | Returns the Selection at the specified index, or null on error. |

## Parameters

| Name  | Type     | Description                           |
|-------|----------|---------------------------------------|
| index | uinteger | The index of the selection to return. |

## Version

Introduced in version August 2014  

