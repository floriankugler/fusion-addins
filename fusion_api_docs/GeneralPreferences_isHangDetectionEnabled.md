# GeneralPreferences.isHangDetectionEnabled Property

Parent Object: [GeneralPreferences](GeneralPreferences.md)  

## Description

Gets and sets whether hang detection is enabled. This is a Windows only setting. If True, Fusion will detect when a task processes for longer than a specific time. A dialog is displayed if a hang is detected, allowing the user to continue processing or stop Fusion and send an error report.

## Syntax

"generalPreferences_var" is a variable referencing a GeneralPreferences object.  

```python
# Get the value of the property.
propertyValue = generalPreferences_var.isHangDetectionEnabled

# Set the value of the property.
generalPreferences_var.isHangDetectionEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version September 2024  

