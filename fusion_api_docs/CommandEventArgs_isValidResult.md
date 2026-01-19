# CommandEventArgs.isValidResult Property

Parent Object: [CommandEventArgs](CommandEventArgs.md)  

## Description

Used during the commandStarting event to get or set that the result of preview is valid and the command can reuse the result when OK is hit. This property should be ignored for all events besides the executePreview event.

## Syntax

"commandEventArgs_var" is a variable referencing a CommandEventArgs object.  

```python
# Get the value of the property.
propertyValue = commandEventArgs_var.isValidResult

# Set the value of the property.
commandEventArgs_var.isValidResult = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

