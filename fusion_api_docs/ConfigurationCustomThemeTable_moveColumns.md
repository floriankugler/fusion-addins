# ConfigurationCustomThemeTable.moveColumns Method

Parent Object: [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md)  

## Description

Moves the specified columns from one table to another.

## Syntax

"configurationCustomThemeTable_var" is a variable referencing a [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md) object.

```python
returnValue = configurationCustomThemeTable_var.moveColumns(columns, targetTable)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationColumn](ConfigurationColumn.md)\[\] | Returns an array of the columns created due to the move. |

## Parameters

| Name | Type | Description |
|----|----|----|
| columns | ConfigurationColumn\[\] | An array of the columns within this table that you want to move. |
| targetTable | [ConfigurationTable](ConfigurationTable.md) | The table you want to move the columns to. The target must be either a top table or a custom theme table. |

## Version

Introduced in version March 2024  

