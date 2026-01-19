# ConfigurationAppearanceColumns.add Method

Parent Object: [ConfigurationAppearanceColumns](ConfigurationAppearanceColumns.md)  

## Description

Adds a new column to the appearance table. If you are adding the first column to the table and it is anything other than the root component, an additional column for the root component will automatically be created as the first column.

## Syntax

"configurationAppearanceColumns_var" is a variable referencing a [ConfigurationAppearanceColumns](ConfigurationAppearanceColumns.md) object.

```python
returnValue = configurationAppearanceColumns_var.add(entity)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationAppearanceColumn](ConfigurationAppearanceColumn.md) | Returns the newly created ConfigurationAppearanceColumn object or null if it fails. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | The root component, occurrence, or body whose appearance will be controlled by this column. |

## Version

Introduced in version March 2024  

