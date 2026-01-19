# CustomGraphicsGroup.id Property

Parent Object: [CustomGraphicsGroup](CustomGraphicsGroup.md)  

## Description

An id you can specify for the entity. By default, all new graphics entities do not have an id and this property will return an empty string. But in cases where entities will be selected, assigning an id can make understanding what was selected much easier.

## Syntax

"customGraphicsGroup_var" is a variable referencing a CustomGraphicsGroup object.  

```python
# Get the value of the property.
propertyValue = customGraphicsGroup_var.id

# Set the value of the property.
customGraphicsGroup_var.id = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version September 2017  

