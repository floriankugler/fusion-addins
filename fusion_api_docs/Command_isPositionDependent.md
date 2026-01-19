# Command.isPositionDependent Property

Parent Object: [Command](Command.md)  

## Description

When working in a parametric design in Fusion and you move any occurrences, those move operations are pending and aren't captured until you use the "Capture Position" command from the POSITION panel or use the "Revert" command from the same panel to move them all back to their original positions. If the design is in a pending situation and you run a command like "Create Sketch", a dialog appears asking if you want to capture the current position or not before continuing. This is because the creation of a sketch can be dependent on the current positions of occurrences in the design. Other commands, like "Fillet", depend directly on model geometry and do not rely on occurrence positions so running the Fillet command does not display the dialog and does not affect the pending state of the occurrences.  

This property allows you to specify if your command is dependent on the current position of occurrences or not. One good way to know if your command is dependent or not is to run the commands in the UI that are equivalent to the API functions you're using and see if the dialog that prompts to save or abort appears. If it does, then you know your command is dependent on occurrence positions.  

If this property is true, then the dialog will appear if there are any pending moved occurrences. The user can choose whether to capture the current changes or abort them, and then your command will continue.  

If you set this property to false, (which is the default), then even if there are pending changes, the occurrences are left in their current positions and your command will run.

## Syntax

"command_var" is a variable referencing a Command object.  

```python
# Get the value of the property.
propertyValue = command_var.isPositionDependent

# Set the value of the property.
command_var.isPositionDependent = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version December 2017  

