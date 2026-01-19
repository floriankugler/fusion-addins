# ConfigurationThemeColumn.deleteMe Method

Parent Object: [ConfigurationThemeColumn](ConfigurationThemeColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationThemeColumn_var" is a variable referencing a [ConfigurationThemeColumn](ConfigurationThemeColumn.md) object.

```python
returnValue = configurationThemeColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

