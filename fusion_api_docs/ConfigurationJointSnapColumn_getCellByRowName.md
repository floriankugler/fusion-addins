# ConfigurationJointSnapColumn.getCellByRowName Method

Parent Object: [ConfigurationJointSnapColumn](ConfigurationJointSnapColumn.md)  

## Description

Gets the cell in this column at the row specified by its name. Depending on the type of data in the cells within the column a ConfigurationFeatureAspectBooleanCell or ConfigurationFeatureAspectStringCell will be returned.

## Syntax

"configurationJointSnapColumn_var" is a variable referencing a [ConfigurationJointSnapColumn](ConfigurationJointSnapColumn.md) object.

```python
returnValue = configurationJointSnapColumn_var.getCellByRowName(rowName)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationCell](ConfigurationCell.md) | Returns the specified cell if successful and null if the name is not found. |

## Parameters

| Name    | Type   | Description                                 |
|---------|--------|---------------------------------------------|
| rowName | string | The name of the row to return the cell for. |

## Version

Introduced in version September 2024  

