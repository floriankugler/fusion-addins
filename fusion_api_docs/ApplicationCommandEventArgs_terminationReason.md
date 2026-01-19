# ApplicationCommandEventArgs.terminationReason Property

Parent Object: [ApplicationCommandEventArgs](ApplicationCommandEventArgs.md)  

## Description

Returns the reason the command is being terminated. This property should be ignored for all events besides the commandTerminated event.

## Syntax

"applicationCommandEventArgs_var" is a variable referencing an ApplicationCommandEventArgs object.  

```python
# Get the value of the property.
propertyValue = applicationCommandEventArgs_var.terminationReason
```

## Property Value

This is a read only property whose value is a [CommandTerminationReason](CommandTerminationReason.md).

## Version

Introduced in version November 2015  

