# ConfigurationParameterCell.value Property

Parent Object: [ConfigurationParameterCell](ConfigurationParameterCell.md)  

## Description

Gets and sets the real value (a double) of the parameter in database units. Setting this property will overwrite any existing expression. This property behaves as read-only when the table is obtained from a DataFile object. This property is only valid for numeric parameters and will fail for text parameters. You can determine the value type of the parameter by using the valueType property. Use the textValue property to get and set the value of text parameters.

## Syntax

"configurationParameterCell_var" is a variable referencing a ConfigurationParameterCell object.  

```python
# Get the value of the property.
propertyValue = configurationParameterCell_var.value

# Set the value of the property.
configurationParameterCell_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version January 2024  

