# ConfigurationAppearanceColumn.getCellByRowId Method

Parent Object: [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationAppearanceColumn_var" is a variable referencing a [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md) object.

```python
returnValue = configurationAppearanceColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationAppearanceCell](ConfigurationAppearanceCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

