# Operation.toolPreset Property

Parent Object: [Operation](Operation.md)  

## Description

Get or set the tool preset to be used. Must be a valid preset of the already assigned tool. Returns null if the operation has no tool or preset.

## Syntax

"operation_var" is a variable referencing an Operation object.  

```python
# Get the value of the property.
propertyValue = operation_var.toolPreset

# Set the value of the property.
operation_var.toolPreset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ToolPreset](ToolPreset.md).

## Version

Introduced in version April 2023  

