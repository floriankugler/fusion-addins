# APIPreferences.defaultPathForScriptsAndAddIns Property

Parent Object: [APIPreferences](APIPreferences.md)  

## Description

The default path where new scripts or add-ins will be created. Scripts will be created in a "Scripts" subdirectory and add-ins will be created in an "AddIns" subdirectory. This must be the full path to the parent folder.  

This path is also where Fusion will look for any scripts and add-ins and automatically display them in the "Scripts and Add-Ins" dialog.

## Syntax

"aPIPreferences_var" is a variable referencing an APIPreferences object.  

```python
# Get the value of the property.
propertyValue = aPIPreferences_var.defaultPathForScriptsAndAddIns

# Set the value of the property.
aPIPreferences_var.defaultPathForScriptsAndAddIns = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version October 2023  

