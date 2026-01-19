# ConfigurationColumns.addPropertyColumn Method

Parent Object: [ConfigurationColumns](ConfigurationColumns.md)  

## Description

Add a new column to control the property inside the component. The component is the owner of the property. This is only valid for TopConfigurationTable. It will fail for all other table types.

## Syntax

"configurationColumns_var" is a variable referencing a [ConfigurationColumns](ConfigurationColumns.md) object.

```python
returnValue = configurationColumns_var.addPropertyColumn(property)
```

## Return Value

| Type | Description |
|----|----|
| [ConfigurationPropertyColumn](ConfigurationPropertyColumn.md) | Returns the new column or null in the case of failure. |

## Parameters

| Name     | Type                     | Description                       |
|----------|--------------------------|-----------------------------------|
| property | [Property](Property.md) | The property to add to the table. |

## Version

Introduced in version March 2024  

