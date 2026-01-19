# ConfigurationFeatureAspectColumn.deleteMe Method

Parent Object: [ConfigurationFeatureAspectColumn](ConfigurationFeatureAspectColumn.md)  

## Description

Deletes this column from the table. Property columns cannot be deleted. If the table was obtained from a DataFile, this method will fail.

## Syntax

"configurationFeatureAspectColumn_var" is a variable referencing a [ConfigurationFeatureAspectColumn](ConfigurationFeatureAspectColumn.md) object.

```python
returnValue = configurationFeatureAspectColumn_var.deleteMe()
```

## Return Value

| Type    | Description                                  |
|---------|----------------------------------------------|
| boolean | Returns true if the deletion was successful. |

## Version

Introduced in version September 2024  

