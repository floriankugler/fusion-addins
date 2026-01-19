# Script.appStoreURL Property

Parent Object: [Script](Script.md)  

## Description

For an add-in installed from the Autodesk App Store, this property returns the URL on the store for the page of this app. This property returns an empty string for all scripts and add-ins not installed from the App Store and if there is a problem determining the URL for an App Store app.

## Syntax

"script_var" is a variable referencing a Script object.  

```python
# Get the value of the property.
propertyValue = script_var.appStoreURL
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version January 2025  

