# Setup.machine Property

Parent Object: [Setup](Setup.md)  

## Description

Gets and sets the Machine associated with the setup. The returned Machine is a transient copy, so the Machine needs to be set to the Setup again to apply any changes.

## Syntax

"setup_var" is a variable referencing a Setup object.  

```python
# Get the value of the property.
propertyValue = setup_var.machine

# Set the value of the property.
setup_var.machine = propertyValue
```

## Property Value

This is a read/write property whose value is a [Machine](Machine.md).

## Version

Introduced in version April 2023  

