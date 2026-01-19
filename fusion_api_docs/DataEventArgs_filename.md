# DataEventArgs.filename Property

Parent Object: [DataEventArgs](DataEventArgs.md)  

## Description

Gets the filename associated with the operation. If there isn't an associated filename, an empty string is returned. For a download operation, this will be the full filename of the downloaded file.

## Syntax

"dataEventArgs_var" is a variable referencing a DataEventArgs object.  

```python
# Get the value of the property.
propertyValue = dataEventArgs_var.filename
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2022  

