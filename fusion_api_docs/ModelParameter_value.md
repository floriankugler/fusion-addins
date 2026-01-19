# ModelParameter.value Property

Parent Object: [ModelParameter](ModelParameter.md)  

## Description

Gets and sets the real value (a double) of the parameter in database units. Setting this property will set/reset the expression value for this parameter.  

This property is only valid for numeric parameters and will fail for text parameters. You can determine the value type of the parameter by using the valueType property. Use the textValue property to get and set the value of text parameters.

## Syntax

"modelParameter_var" is a variable referencing a ModelParameter object.  

```python
# Get the value of the property.
propertyValue = modelParameter_var.value

# Set the value of the property.
modelParameter_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version November 2014  

