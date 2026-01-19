# ConfigurationMaterialColumn.deleteMe Method

Parent Object: [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationMaterialColumn_var" is a variable referencing a [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md) object.

```python
returnValue = configurationMaterialColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version March 2024  

