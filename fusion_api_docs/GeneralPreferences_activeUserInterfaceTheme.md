# GeneralPreferences.activeUserInterfaceTheme Property

Parent Object: [GeneralPreferences](GeneralPreferences.md)  

## Description

Gets the active user interface theme. This property is only different from userInterfaceTheme in the case the theme is DeviceUserInterfaceTheme. In that case the theme used will be returned.

## Syntax

"generalPreferences_var" is a variable referencing a GeneralPreferences object.  

```python
# Get the value of the property.
propertyValue = generalPreferences_var.activeUserInterfaceTheme
```

## Property Value

This is a read only property whose value is a [UserInterfaceThemes](UserInterfaceThemes.md).

## Version

Introduced in version January 2026  

