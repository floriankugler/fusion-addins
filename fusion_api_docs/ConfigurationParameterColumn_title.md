# ConfigurationParameterColumn.title Property

Parent Object: [ConfigurationParameterColumn](ConfigurationParameterColumn.md)  

## Description

The title of this column. In a top table, this can only be edited for suppression, visibility, parameter, and theme table columns. It behaves as read-only for all other types. In a theme table, the title of all the columns can be modified except for the column that represents the root component for materials and appearances.  

If the table was obtained from a DataFile, this property behaves as read-only for all the columns.

## Syntax

"configurationParameterColumn_var" is a variable referencing a ConfigurationParameterColumn object.  

```python
# Get the value of the property.
propertyValue = configurationParameterColumn_var.title

# Set the value of the property.
configurationParameterColumn_var.title = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2024  

