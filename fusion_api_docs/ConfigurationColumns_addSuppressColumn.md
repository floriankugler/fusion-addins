# ConfigurationColumns.addSuppressColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Adds a new column to control the suppression of a feature. The term "feature" is used broadly and includes anything displayed in the timeline. If a suppression column already exists for the feature, the existing column is returned.  

This is only valid for TopConfigurationTable and ThemeConfigurationTable objects. It will fail for all other table types.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addSuppressColumn(feature)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationSuppressColumn](ConfigurationSuppressColumn.md) | Returns the new column or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| feature | [Base](Base.md) | The feature to add to the table. Any object that is displayed in the timeline can be used as input. For example, some valid objects are any modeling features, sketches, construction geometry, and joints. |

## Version

Introduced in version March 2024  

