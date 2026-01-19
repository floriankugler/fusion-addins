# Attribute.value Property

Parent Object: [Attribute](Attribute.md)  

## Description

Gets and sets the value of this attribute.  

The size of an attribute value is limited to 2MB (2097152 bytes). If you need to save data that is larger than 2MB you'll need to break the data into pieces and save it in multiple attributes.

## Syntax

"attribute_var" is a variable referencing an Attribute object.  

```python
# Get the value of the property.
propertyValue = attribute_var.value

# Set the value of the property.
attribute_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version May 2016  

