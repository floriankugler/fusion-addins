# TableCommandInput.removeInput Method

Parent Object: [TableCommandInput](TableCommandInput.md)  

## Description

Removes the command input that is at the specified row and column. This doesn't delete the command input from the collection of inputs associated with the command but just removes it from being displayed in the table.

## Syntax

"tableCommandInput_var" is a variable referencing a [TableCommandInput](TableCommandInput.md) object.

```python
returnValue = tableCommandInput_var.removeInput(row, column)
```

## Return Value

| Type    | Description                                 |
|---------|---------------------------------------------|
| boolean | Returns true if the removal was successful. |

## Parameters

| Name   | Type    | Description                                               |
|--------|---------|-----------------------------------------------------------|
| row    | integer | The row where the command input to be removed is located. |
| column | integer | The row where the command input to be removed is located. |

## Version

Introduced in version September 2016  

