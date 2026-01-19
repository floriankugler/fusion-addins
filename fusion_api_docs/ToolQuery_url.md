# ToolQuery.url Property

Parent Object: [ToolQuery](ToolQuery.md)  

## Description

The URL specifies the location and folder to search for in the Tool library. Setting the URL updates the location. When searching inside a ToolLibrary the URL will be ignored.

## Syntax

"toolQuery_var" is a variable referencing a ToolQuery object.  

```python
# Get the value of the property.
propertyValue = toolQuery_var.url

# Set the value of the property.
toolQuery_var.url = propertyValue
```

## Property Value

This is a read/write property whose value is a [URL](URL.md).

## Version

Introduced in version April 2023  

