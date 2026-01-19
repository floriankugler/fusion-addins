# FloatProperty.values Property

Parent Object: [FloatProperty](FloatProperty.md)  

## Description

Gets and sets the values associated with this property. HasMultipleValues property indicates if this property will be returning more than one value.  

This is most commonly used for properties associated with materials and appearances.

## Syntax

"floatProperty_var" is a variable referencing a FloatProperty object.  

```python
# Get the value of the property.
propertyValue = floatProperty_var.values

# Set the value of the property.
floatProperty_var.values = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type double.

## Version

Introduced in version August 2014  

