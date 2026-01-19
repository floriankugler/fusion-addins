# ConfigurationJointSnapColumn.deleteMe Method

Parent Object: [ConfigurationJointSnapColumn](ConfigurationJointSnapColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationJointSnapColumn_var" is a variable referencing a [ConfigurationJointSnapColumn](ConfigurationJointSnapColumn.md) object.

```python
returnValue = configurationJointSnapColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version September 2024  

