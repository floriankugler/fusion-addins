# TableCommandInput.getInputAtPosition Method

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Returns the command input that is in the specified row and column. In the case where a command input spans multiple columns, the same input can be returned from multiple positions.

## Syntax

"tableCommandInput_var" is a variable referencing a [TableCommandInput](TableCommandInput.md) object.

```python
returnValue = tableCommandInput_var.getInputAtPosition(row, column)
```

## Return Value

| Type | Description |
|----|----|
| [CommandInput](CommandInput.md) | Returns the command input that is in the specified row and column. If there isn't a command input in the specified location, null is returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| row | integer | The row index to return the command input from where the first row is 0. |
| column | integer | The row index to return the command input from where the first row is 0. |

## Version

Introduced in version November 2016  

