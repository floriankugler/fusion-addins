# Script.isVisible Property

Parent Object: [Script](Script.md)  

## Description

Gets and sets whether the script or add-in is visible within the “Scripts and Add-Ins” dialog. By default, all scripts and add-ins are visible. Setting this to false will cause it to be hidden and unloaded if it is already running. Also, if it’s an add-in set to load on startup, it will no longer be loaded.

## Syntax

"script_var" is a variable referencing a Script object.  

```python
# Get the value of the property.
propertyValue = script_var.isVisible

# Set the value of the property.
script_var.isVisible = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version October 2023  

