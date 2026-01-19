# ConfigurationParameterCell.textValue Property

Parent Object: [ConfigurationParameterCell](ConfigurationParameterCell.md)  

## Description

Gets and sets the text value of the parameter when it is a text parameter. This can be determined by checking the valueType property. Setting this value will cause the current expression to be overwritten. This property behaves as read-only when the table is obtained from a DataFile object.

## Syntax

"configurationParameterCell_var" is a variable referencing a ConfigurationParameterCell object.  

```python
# Get the value of the property.
propertyValue = configurationParameterCell_var.textValue

# Set the value of the property.
configurationParameterCell_var.textValue = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2026  

