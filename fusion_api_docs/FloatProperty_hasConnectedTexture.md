# FloatProperty.hasConnectedTexture Property

Parent Object: [FloatProperty](FloatProperty.md)  

## Description

When the property is associated with an appearance this indicates if the float value has been overridden using a texture. Setting this property to False will remove the texture so that a float value is used. Setting this property to True will connect a texture to this float value. For properties not associated with an appearance, this acts as read-only and always returns false.

## Syntax

"floatProperty_var" is a variable referencing a FloatProperty object.  

```python
# Get the value of the property.
propertyValue = floatProperty_var.hasConnectedTexture

# Set the value of the property.
floatProperty_var.hasConnectedTexture = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

