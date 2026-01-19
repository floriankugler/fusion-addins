# ConfigurationCustomThemeTables.add Method

Parent Object: [ConfigurationCustomThemeTables](ConfigurationCustomThemeTables.md)  

## Description

Creates a new custom theme table using the specified columns.

## Syntax

"configurationCustomThemeTables_var" is a variable referencing a [ConfigurationCustomThemeTables](ConfigurationCustomThemeTables.md) object.

```python
returnValue = configurationCustomThemeTables_var.add(columns)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md) | Returns the newly created ConfigurationCustomThemeTable or null if the creation fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| columns | ConfigurationColumn\[\] | An array of ConfigurationColumn objects used to create a new custom theme table. The columns must exist within the top configuration table, and they cannot include any ConfigurationThemeColumn, ConfigurationPropertyColumn, ConfigurationAppearanceColumn, ConfigurationMaterialColumn, ConfigurationPlasticRuleColumn, or ConfigurationSheetMetalRuleColumn objects. The specified columns will be removed from the main table, and a new ConfigurationThemeColumn will be created in the top table to reference the newly created custom theme table. |

## Version

Introduced in version March 2024  

