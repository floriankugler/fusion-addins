# Parameter.textValue Property

Parent Object: [Parameter](Parameter.md)  

## Description

Gets and sets the value of the parameter when it is a text parameter. This can be determined by checking the valueType property. Setting this value will cause the current expression to be overwritten. If the parameter is not a text parameter, the value of this property should be ignored and setting will fail.

## Syntax

"parameter_var" is a variable referencing a Parameter object.  

```python
# Get the value of the property.
propertyValue = parameter_var.textValue

# Set the value of the property.
parameter_var.textValue = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2025  

