# FloatProperty.hasLimits Property

Parent Object: [FloatProperty](FloatProperty.md)  

## Description

Gets the boolean flag that indicates if the value of this property has any limits it must be within to be valid. If True, use the GetLimits method to get the limit values.  

This is most commonly used for properties associated with materials and appearances and in most cases will return false.

## Syntax

"floatProperty_var" is a variable referencing a FloatProperty object.  

```python
# Get the value of the property.
propertyValue = floatProperty_var.hasLimits
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version August 2014  

