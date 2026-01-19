# ConfigurationAppearanceCell.appearance Property

Parent Object: [ConfigurationAppearanceCell](ConfigurationAppearanceCell.md)  

## Description

Gets and sets the appearance associated with this cell. This property can return null indicating the appearance from the physical material assigned to the object is inherited. Setting the property to null will inherit the appearance from the physical material assigned to the object.

## Syntax

"configurationAppearanceCell_var" is a variable referencing a ConfigurationAppearanceCell object.  

```python
# Get the value of the property.
propertyValue = configurationAppearanceCell_var.appearance

# Set the value of the property.
configurationAppearanceCell_var.appearance = propertyValue
```

## Property Value

This is a read/write property whose value is an [Appearance](Appearance.md).

## Version

Introduced in version January 2024  

