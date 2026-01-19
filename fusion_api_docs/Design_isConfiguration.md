# Design.isConfiguration Property

Parent Object: [Design](Design.md)  

## Description

Gets if this design is a configuration. If this returns true, the configurationRowId can be used to get the row used to define this configuration. Also, when this is true, the design is essentially read-only and edits are either blocked from taking place or cannot be saved.

## Syntax

"design_var" is a variable referencing a Design object.  

```python
# Get the value of the property.
propertyValue = design_var.isConfiguration
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version January 2024  

