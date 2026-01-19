# ConfigurationSuppressColumn.deleteMe Method

Parent Object: [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationSuppressColumn_var" is a variable referencing a [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md) object.

```python
returnValue = configurationSuppressColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

