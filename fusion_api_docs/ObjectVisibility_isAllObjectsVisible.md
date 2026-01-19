# ObjectVisibility.isAllObjectsVisible Property

Parent Object: [ObjectVisibility](ObjectVisibility.md)  

## Description

Sets if all objects are visible or hidden. When setting this property it will set the value of all other properties of this object to true or false. When getting this property, if it is true, then all other properties are true. If false, one or more other properties are false.

## Syntax

"objectVisibility_var" is a variable referencing an ObjectVisibility object.  

```python
# Get the value of the property.
propertyValue = objectVisibility_var.isAllObjectsVisible

# Set the value of the property.
objectVisibility_var.isAllObjectsVisible = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2025  

