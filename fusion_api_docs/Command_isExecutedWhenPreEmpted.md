# Command.isExecutedWhenPreEmpted Property

Parent Object: [Command](Command.md)  

## Description

Specifies what the behavior will be when a command is preempted by the user executing another command. If true (the default), and all of the current inputs are valid, the command will be executed just the same as if the user clicked the OK button. If false, the command is terminated.

## Syntax

"command_var" is a variable referencing a Command object.  

```python
# Get the value of the property.
propertyValue = command_var.isExecutedWhenPreEmpted

# Set the value of the property.
command_var.isExecutedWhenPreEmpted = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2015  

