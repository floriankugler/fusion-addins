# CommandEventArgs.executeFailedMessage Property

Parent Object: [CommandEventArgs](CommandEventArgs.md)  

## Description

Used during the execute event to get or set a description of an execute failure. This property should be ignored for all events besides the Execute event.

## Syntax

"commandEventArgs_var" is a variable referencing a CommandEventArgs object.  

```python
# Get the value of the property.
propertyValue = commandEventArgs_var.executeFailedMessage

# Set the value of the property.
commandEventArgs_var.executeFailedMessage = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version August 2014  

