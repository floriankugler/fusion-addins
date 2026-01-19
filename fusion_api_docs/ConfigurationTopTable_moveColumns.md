# ConfigurationTopTable.moveColumns Method

Parent Object: [ConfigurationTopTable](ConfigurationTopTable.md)  

## Description

Moves the specified columns from one table to another.

## Syntax

"configurationTopTable_var" is a variable referencing a [ConfigurationTopTable](ConfigurationTopTable.md) object.

```python
returnValue = configurationTopTable_var.moveColumns(columns, targetTable)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationColumn](ConfigurationColumn.md)\[\] | Returns an array of the columns created due to the move. |

## Parameters

| Name | Type | Description |
|----|----|----|
| columns | ConfigurationColumn\[\] | An array of the columns within the top table you want to move. |
| targetTable | [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md) | The table you want to move the columns to. The target must be a custom theme table. |

## Version

Introduced in version March 2024  

