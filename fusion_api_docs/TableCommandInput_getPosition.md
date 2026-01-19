# TableCommandInput.getPosition Method

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Gets the position of the specified command input within the table.

## Syntax

"tableCommandInput_var" is a variable referencing a [TableCommandInput](TableCommandInput.md) object.  

```python
(returnValue, row, column, rowSpan, columnSpan) = tableCommandInput_var.getPosition(input)
```

## Return Value

| Type    | Description                                             |
|---------|---------------------------------------------------------|
| boolean | Returns true if the position was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CommandInput](CommandInput.md) | The existing command input you want to find the associated cell for. |
| row | integer | The returned row index of the cell. |
| column | integer | The returned column index of the cell. |
| rowSpan | integer | The returned number of additional rows used by the input. A value of 0 indicates that no additional rows are used. |
| columnSpan | integer | The returned number of additional columns used by the input. A value of 0 indicates that no additional columns are used. |

## Version

Introduced in version September 2016  

