# ConfigurationInsertColumn.deleteMe Method

Parent Object: [ConfigurationInsertColumn](ConfigurationInsertColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationInsertColumn_var" is a variable referencing a [ConfigurationInsertColumn](ConfigurationInsertColumn.md) object.

```python
returnValue = configurationInsertColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

