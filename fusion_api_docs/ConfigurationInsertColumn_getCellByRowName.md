# ConfigurationInsertColumn.getCellByRowName Method

Parent Object: [ConfigurationInsertColumn](ConfigurationInsertColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationInsertColumn_var" is a variable referencing a [ConfigurationInsertColumn](ConfigurationInsertColumn.md) object.

```python
returnValue = configurationInsertColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationInsertCell](ConfigurationInsertCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

