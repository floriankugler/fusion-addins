# IntegerProperty.value Property

Parent Object: [IntegerProperty](IntegerProperty.md)  

## Description

Gets and sets this property value. The value of this property should be ignored if the HasConnectedTexture property is true. Setting this will remove any associated texture, if there is one.

## Syntax

"integerProperty_var" is a variable referencing an IntegerProperty object.  

```python
# Get the value of the property.
propertyValue = integerProperty_var.value

# Set the value of the property.
integerProperty_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version August 2014  

