# ConfigurationColumns.addVisibilityColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Adds a new column to control the visibility of an entity. If a visibility column already exists for the entity, the existing column is returned.  

This is only valid for ConfigurationTopTable and ConfigurationCustomThemeTable objects and will fail for all other table types.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addVisibilityColumn(entity)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationVisibilityColumn](ConfigurationVisibilityColumn.md) | Returns the new column or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | Returns the entity whose visibility will be controlled by this column. |

## Version

Introduced in version March 2024  

