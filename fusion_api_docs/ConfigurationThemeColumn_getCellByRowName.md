# ConfigurationThemeColumn.getCellByRowName Method

Parent Object: [ConfigurationThemeColumn](ConfigurationThemeColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationThemeColumn_var" is a variable referencing a [ConfigurationThemeColumn](ConfigurationThemeColumn.md) object.

```python
returnValue = configurationThemeColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationThemeCell](ConfigurationThemeCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

