# ToolQuery.location Property

Parent Object: [ToolQuery](ToolQuery.md)  

## Description

Specifies the location to search in the Tool library. Setting the location clears any previous specified URL. When searching inside a ToolLibrary the location will be ignored.

## Syntax

"toolQuery_var" is a variable referencing a ToolQuery object.  

```python
# Get the value of the property.
propertyValue = toolQuery_var.location

# Set the value of the property.
toolQuery_var.location = propertyValue
```

## Property Value

This is a read/write property whose value is a [LibraryLocations](LibraryLocations.md).

## Version

Introduced in version April 2023  

