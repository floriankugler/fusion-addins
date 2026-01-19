# TabCommandInput.resourceFolder Property

Parent Object: [TabCommandInput](TabCommandInput.md)  

## Description

Gets the folder that contains the icon for the tab. If no name is specified (no text on tab), a resourceFolder containing the icon needs to be provided. Icons can be defined using either PNG or SVG files. More information about icons can be found in the user manual topic [User Interface Customization](UserInterface_UM.htm#IconsForCommands).

## Syntax

"tabCommandInput_var" is a variable referencing a TabCommandInput object.  

```python
# Get the value of the property.
propertyValue = tabCommandInput_var.resourceFolder
```

## Property Value

This is a read only property whose value is a string.

## Version

Introduced in version July 2015  

