# ConfigurationParameterCell.expression Property

Parent Object: [ConfigurationParameterCell](ConfigurationParameterCell.md)  

## Description

Gets and sets the expression that defines the value of the associated parameter when the parent row is active. This works for both numeric and text parameters. This property behaves as read-only when the table is obtained from a DataFile object.

## Syntax

"configurationParameterCell_var" is a variable referencing a ConfigurationParameterCell object.  

```python
# Get the value of the property.
propertyValue = configurationParameterCell_var.expression

# Set the value of the property.
configurationParameterCell_var.expression = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2024  

