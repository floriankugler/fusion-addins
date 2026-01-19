# ConfigurationMaterialColumn.getCellByRowId Method

Parent Object: [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md)  

## Description

Gets the cell in this column at the row specified by its ID.

## Syntax

"configurationMaterialColumn_var" is a variable referencing a [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md) object.

```python
returnValue = configurationMaterialColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationMaterialCell](ConfigurationMaterialCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version January 2024  

