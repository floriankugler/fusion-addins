# CommandControl.isPromotedByDefault Property

Parent Object: [CommandControl](CommandControl.md)  

## Description

Gets or sets if this command is a default command in the panel. This defines the default state of the panel if the UI is reset. This property is ignored in the case where this control isn't in a panel.  

The promote method provides more options over how the control is promoted.

## Syntax

"commandControl_var" is a variable referencing a CommandControl object.  

```python
# Get the value of the property.
propertyValue = commandControl_var.isPromotedByDefault

# Set the value of the property.
commandControl_var.isPromotedByDefault = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

