# ValueInput.objectReference Property

Parent Object: [ValueInput](ValueInput.md)  

## Description

Gets the object being referenced, if there is one. Returns null AND GetLastError returns ValueNotOfType if there is no object reference. You can use the valueType property to determine which value type is currently used.

## Syntax

"valueInput_var" is a variable referencing a ValueInput object.  

```python
# Get the value of the property.
propertyValue = valueInput_var.objectReference
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2016  

