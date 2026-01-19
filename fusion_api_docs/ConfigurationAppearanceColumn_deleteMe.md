# ConfigurationAppearanceColumn.deleteMe Method

Parent Object: [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationAppearanceColumn_var" is a variable referencing a [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md) object.

```python
returnValue = configurationAppearanceColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

