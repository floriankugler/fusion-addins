# ConfigurationParameterColumn.getCellByRowName Method

Parent Object: [ConfigurationParameterColumn](ConfigurationParameterColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationParameterColumn_var" is a variable referencing a [ConfigurationParameterColumn](ConfigurationParameterColumn.md) object.

```python
returnValue = configurationParameterColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationParameterCell](ConfigurationParameterCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

