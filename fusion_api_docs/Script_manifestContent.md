# Script.manifestContent Property

Parent Object: [Script](Script.md)  

## Description

Gets the full contents of the manifest file associated with this script or add-in. This is particularly useful if you have any custom information defined in the manifest. The manifest file uses JSON to format its content.

## Syntax

"script_var" is a variable referencing a Script object.  

```python
# Get the value of the property.
propertyValue = script_var.manifestContent
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version October 2023  

