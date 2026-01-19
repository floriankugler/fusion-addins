# ConfigurationColumn.deleteMe Method

Parent Object: [ConfigurationColumn](ConfigurationColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationColumn_var" is a variable referencing a [ConfigurationColumn](ConfigurationColumn.md) object.

```python
returnValue = configurationColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

