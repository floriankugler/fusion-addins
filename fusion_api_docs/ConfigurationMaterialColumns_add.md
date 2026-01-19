# ConfigurationMaterialColumns.add Method

Parent Object: [ConfigurationMaterialColumns](ConfigurationMaterialColumns.md)  

## Description

Adds a new column to the material table. If you are adding the first column to the table and it is anything other than the root component, an additional column for the root component will automatically be created as the first column.

## Syntax

"configurationMaterialColumns_var" is a variable referencing a [ConfigurationMaterialColumns](ConfigurationMaterialColumns.md) object.

```python
returnValue = configurationMaterialColumns_var.add(entity)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationMaterialColumn](ConfigurationMaterialColumn.md) | Returns the newly created ConfigurationMaterialColumn object or null if it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | The component or body whose material will be controlled by this column. |

## Version

Introduced in version March 2024  

