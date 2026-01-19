# ValueInput.stringValue Property

Parent Object: [ValueInput](ValueInput.md)  

## Description

Gets the string value, if there is one. Returns an empty string AND GetLastError returns ValueNotOfType if there is no string value. You can use the valueType property to determine which value type is currently used.

## Syntax

"valueInput_var" is a variable referencing a ValueInput object.  

```python
# Get the value of the property.
propertyValue = valueInput_var.stringValue
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version August 2014  

