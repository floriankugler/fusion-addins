# SharedLink.isShared Property

Parent Object: [SharedLink](SharedLink.md)  

## Description

Gets and sets if a shared link should be made available for this DataFile. This property defaults to false for a new DataFile. Setting it to true will allow the URL for the file to be obtained. Setting it to false will restrict access to the URL and block access for anyone currently using it. In other words, this is a dynamic setting and doesn't just control getting the link URL.

## Syntax

"sharedLink_var" is a variable referencing a SharedLink object.  

```python
# Get the value of the property.
propertyValue = sharedLink_var.isShared

# Set the value of the property.
sharedLink_var.isShared = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2024  

