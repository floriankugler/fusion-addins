# SharedLink.isPasswordRequired Property

Parent Object: [SharedLink](SharedLink.md)  

## Description

Gets if a password is required to access the file's web page using the link URL. This property can be set to false to turn off the password requirement. It cannot be set to true. To enable a password, use the setPassword method, which sets the password and has the side effect of setting this property to true.

## Syntax

"sharedLink_var" is a variable referencing a SharedLink object.  

```python
# Get the value of the property.
propertyValue = sharedLink_var.isPasswordRequired

# Set the value of the property.
sharedLink_var.isPasswordRequired = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2024  

