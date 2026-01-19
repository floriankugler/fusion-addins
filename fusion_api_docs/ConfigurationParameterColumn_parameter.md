# ConfigurationParameterColumn.parameter Property

Parent Object: [ConfigurationParameterColumn](ConfigurationParameterColumn.md)  

## Description

Returns the parameter being controlled by this column.  

This property returns null when the table being queried was obtained from a DataFile object.

## Syntax

"configurationParameterColumn_var" is a variable referencing a ConfigurationParameterColumn object.  

```python
# Get the value of the property.
propertyValue = configurationParameterColumn_var.parameter
```

## Property Value

This is a read only property whose value is a [Parameter](Parameter.md).

## Version

Introduced in version January 2024  

