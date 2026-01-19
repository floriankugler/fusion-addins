# ApplicationCommandEventArgs.isCanceled Property

Parent Object: [ApplicationCommandEventArgs](ApplicationCommandEventArgs.md)  

## Description

Used during the commandStarting event to get or set if the command should be allowed to continue executing or be canceled. This defaults to false, which will allow the command to execute. Setting this to true will cancel the command and not begin the execution. This property should be ignored for all events besides the commandStarting event.

## Syntax

"applicationCommandEventArgs_var" is a variable referencing an ApplicationCommandEventArgs object.  

```python
# Get the value of the property.
propertyValue = applicationCommandEventArgs_var.isCanceled

# Set the value of the property.
applicationCommandEventArgs_var.isCanceled = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2015  

