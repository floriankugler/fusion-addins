# ConfigurationVisibilityColumn.getCellByRowName Method

Parent Object: [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationVisibilityColumn_var" is a variable referencing a [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md) object.

```python
returnValue = configurationVisibilityColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationVisibilityCell](ConfigurationVisibilityCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

