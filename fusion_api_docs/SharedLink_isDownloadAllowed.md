# SharedLink.isDownloadAllowed Property

Parent Object: [SharedLink](SharedLink.md)  

## Description

Specifies if the user with the shared link can download the file or only view it. Changing this setting changes the behavior of the existing link. When a DataFile is shared, and a link is created, this defaults to true, allowing anyone with the link to download the file.

## Syntax

"sharedLink_var" is a variable referencing a SharedLink object.  

```python
# Get the value of the property.
propertyValue = sharedLink_var.isDownloadAllowed

# Set the value of the property.
sharedLink_var.isDownloadAllowed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version May 2024  

