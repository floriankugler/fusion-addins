# ValueInput.booleanValue Property

Parent Object: [ValueInput](ValueInput.md)  

## Description

Gets the boolean value, if there is one. Returns false AND GetLastError returns ValueNotOfType if there is no boolean value. You can use the valueType property to determine which value type is currently used.

## Syntax

"valueInput_var" is a variable referencing a ValueInput object.  

```python
# Get the value of the property.
propertyValue = valueInput_var.booleanValue
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version May 2020  

