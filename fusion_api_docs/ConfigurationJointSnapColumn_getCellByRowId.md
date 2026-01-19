# ConfigurationJointSnapColumn.getCellByRowId Method

Parent Object: [ConfigurationJointSnapColumn](ConfigurationJointSnapColumn.md)  

## Description

This method returns the cell in this column at the row identified by its ID. Depending on the type of data in the cells within the column, a ConfigurationFeatureAspectBooleanCell or ConfigurationFeatureAspectStringCell will be returned.

## Syntax

"configurationJointSnapColumn_var" is a variable referencing a [ConfigurationJointSnapColumn](ConfigurationJointSnapColumn.md) object.

```python
returnValue = configurationJointSnapColumn_var.getCellByRowId(rowId)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationCell](ConfigurationCell.md) | Returns the specified cell if successful and null if the id is not found. |

## Parameters

| Name  | Type   | Description                               |
|-------|--------|-------------------------------------------|
| rowId | string | The ID of the row to return the cell for. |

## Version

Introduced in version September 2024  

