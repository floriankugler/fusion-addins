# ConfigurationRow.name Property

Parent Object: [ConfigurationRow](ConfigurationRow.md)  

## Description

Gets and sets the name of this row. Names must be unique with respect to other rows in this table. If you specify a name that exists, Fusion will append a counter to ensure uniqueness. For example, if "Small" is already used and you name another row "Small", you will end up with "Small (1)".

## Syntax

"configurationRow_var" is a variable referencing a ConfigurationRow object.  

```python
# Get the value of the property.
propertyValue = configurationRow_var.name

# Set the value of the property.
configurationRow_var.name = propertyValue
```

## Property Value

This is a read/write property whose value is a string.

## Version

Introduced in version January 2024  

