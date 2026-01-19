# CommandEventArgs.terminationReason Property

Parent Object: [CommandEventArgs](CommandEventArgs.md)  

## Description

Gets the termination reason of the command. It's only valid on the destroy event.

## Syntax

"commandEventArgs_var" is a variable referencing a CommandEventArgs object.  

```python
# Get the value of the property.
propertyValue = commandEventArgs_var.terminationReason
```

## Property Value

This is a read only property whose value is a [CommandTerminationReason](CommandTerminationReason.md).

## Version

Introduced in version June 2015  

