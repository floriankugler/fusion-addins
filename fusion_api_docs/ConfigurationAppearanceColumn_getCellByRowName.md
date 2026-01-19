# ConfigurationAppearanceColumn.getCellByRowName Method

Parent Object: [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md)  

## Description

Gets the cell in this column at the row specified by its name.

## Syntax

"configurationAppearanceColumn_var" is a variable referencing a [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md) object.

```python
returnValue = configurationAppearanceColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationAppearanceCell](ConfigurationAppearanceCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version January 2024  

