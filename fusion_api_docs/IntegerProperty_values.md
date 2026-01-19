# IntegerProperty.values Property

Parent Object: [IntegerProperty](IntegerProperty.md)  

## Description

Gets and sets the values associated with this property. HasMultipleValues property indicates if this property will be returning more than one value.  

This is most commonly used for properties associated with materials and appearances.

## Syntax

"integerProperty_var" is a variable referencing an IntegerProperty object.  

```python
# Get the value of the property.
propertyValue = integerProperty_var.values

# Set the value of the property.
integerProperty_var.values = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type integer.

## Version

Introduced in version August 2014  

