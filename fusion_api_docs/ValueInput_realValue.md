# ValueInput.realValue Property

Parent Object: [ValueInput](ValueInput.md)  

## Description

Gets the real value, if there is one. Returns -1 AND GetLastError returns ValueNotOfType if there is no real value. You can use the valueType property to determine which value type is currently used.

## Syntax

"valueInput_var" is a variable referencing a ValueInput object.  

```python
# Get the value of the property.
propertyValue = valueInput_var.realValue
```

## Property Value

This is a read only property whose value is a double.

## Version

Introduced in version August 2014  

