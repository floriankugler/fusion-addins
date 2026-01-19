# ConfigurationVisibilityColumn.deleteMe Method

Parent Object: [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationVisibilityColumn_var" is a variable referencing a [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md) object.

```python
returnValue = configurationVisibilityColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

