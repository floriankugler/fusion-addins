# ConfigurationPropertyColumn.getCellByRowName Method

Parent Object: [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationPropertyColumn_var" is a variable referencing a [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md) object.

```python
returnValue = configurationPropertyColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPropertyCell](ConfigurationPropertyCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

