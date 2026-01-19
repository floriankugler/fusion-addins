# ConfigurationJointSnapCell.snap Property

Parent Object: [ConfigurationJointSnapCell](ConfigurationJointSnapCell.md)  

## Description

Gets and sets which snap will be used when the row this cell is in is active. When setting this property, only snaps defined for the parent column of this cell can be used.

## Syntax

"configurationJointSnapCell_var" is a variable referencing a ConfigurationJointSnapCell object.  

```python
# Get the value of the property.
propertyValue = configurationJointSnapCell_var.snap

# Set the value of the property.
configurationJointSnapCell_var.snap = propertyValue
```

## Property Value

This is a read/write property whose value is a [ConfigurationJointSnap](ConfigurationJointSnap.md).

## Version

Introduced in version September 2024  

