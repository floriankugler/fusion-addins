# CommandEventArgs.executeFailed Property

Parent Object: [CommandEventArgs](CommandEventArgs.md)  

## Description

Used during the execute event to get or set that the execute operations failed and the commands transaction should be aborted. This property should be ignored for all events besides the Execute event.

## Syntax

"commandEventArgs_var" is a variable referencing a CommandEventArgs object.  

```python
# Get the value of the property.
propertyValue = commandEventArgs_var.executeFailed

# Set the value of the property.
commandEventArgs_var.executeFailed = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version August 2014  

