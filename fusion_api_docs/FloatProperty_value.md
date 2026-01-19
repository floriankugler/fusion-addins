# FloatProperty.value Property

Parent Object: [FloatProperty](FloatProperty.md)  

## Description

Gets and sets this property value. The value of this property should be ignored if the HasConnectedTexture property is true. Setting this will remove any associated texture, if there is one.

## Syntax

"floatProperty_var" is a variable referencing a FloatProperty object.  

```python
# Get the value of the property.
propertyValue = floatProperty_var.value

# Set the value of the property.
floatProperty_var.value = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  

