# IntegerProperty.parent Property

Parent Object: [IntegerProperty](IntegerProperty.md)  

## Description

Returns the parent of this property.For properties associated with an appearance this will return the parent Appearance. For properties associated with a material, this will return the parent Material. For other types of properties, this will return the PropertyGroup it is in.

## Syntax

"integerProperty_var" is a variable referencing an IntegerProperty object.  

```python
# Get the value of the property.
propertyValue = integerProperty_var.parent
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version August 2014  

