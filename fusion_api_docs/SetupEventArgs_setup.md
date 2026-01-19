# SetupEventArgs.setup Property

Parent Object: [SetupEventArgs](SetupEventArgs.md)  

## Description

Provides access to the setup. Can be null in the case where the event is fired before the setup has been created or after it has been deleted.

## Syntax

"setupEventArgs_var" is a variable referencing a SetupEventArgs object.  

```python
# Get the value of the property.
propertyValue = setupEventArgs_var.setup
```

## Property Value

This is a read only property whose value is a [Setup](Setup.md).

## Version

Introduced in version April 2023  

