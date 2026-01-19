# ConfigurationPropertyColumn.deleteMe Method

Parent Object: [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationPropertyColumn_var" is a variable referencing a [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md) object.

```python
returnValue = configurationPropertyColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

