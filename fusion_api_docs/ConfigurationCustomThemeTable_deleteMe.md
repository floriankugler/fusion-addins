# ConfigurationCustomThemeTable.deleteMe Method

Parent Object: [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md)  

## Description

Deletes this custom theme table from the configuration.

## Syntax

"configurationCustomThemeTable_var" is a variable referencing a [ConfigurationCustomThemeTable](ConfigurationCustomThemeTable.md) object.

```python
returnValue = configurationCustomThemeTable_var.deleteMe(deleteColumns)
```

## Return Value

| Type    | Description                                |
|---------|--------------------------------------------|
| boolean | Returns true if the delete was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| deleteColumns | boolean | If true, this deletes the columns in the custom theme table. If false, it moves them back to the top table. |

## Version

Introduced in version March 2024  

