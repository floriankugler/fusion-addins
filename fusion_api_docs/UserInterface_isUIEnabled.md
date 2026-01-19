# UserInterface.isUIEnabled Property

Parent Object: [UserInterface](UserInterface.md)  

## Description

Gets and sets if the Fusion user interface is enabled or not. By default it is enabled allowing the user to interact with Fusion. When set to false, the UI is disabled which blocks all interaction, including running commands, manipulating the view and interacting with the browser.

## Syntax

"userInterface_var" is a variable referencing a UserInterface object.  

```python
# Get the value of the property.
propertyValue = userInterface_var.isUIEnabled

# Set the value of the property.
userInterface_var.isUIEnabled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2025  

