# Application.userId Property

Parent Object: [Application](Application.md)  

## Description

Returns the internal name of the Autodesk account currently logged in. This can be used by applications sold through the Autodesk Exchange Store to verify that the user has in fact purchased the product.

## Syntax

"application_var" is a variable referencing an Application object.  

```python
# Get the value of the property.
propertyValue = application_var.userId
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version September 2015  

