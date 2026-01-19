# Command.isAutoExecute Property

Parent Object: [Command](Command.md)  

## Description

Gets and sets whether this command will automatically execute if no command inputs have been defined. If any command inputs have been created, the value of this property is ignored and the command dialog will be displayed and the command will execute when the user clicks 'OK'. if no command inputs have been defined and this is set to False, then the command will not execute but will remain running.  

The default value for this property is true so that the command will execute if no command inputs have been defined.

## Syntax

"command_var" is a variable referencing a Command object.  

```python
# Get the value of the property.
propertyValue = command_var.isAutoExecute

# Set the value of the property.
command_var.isAutoExecute = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version April 2017  

