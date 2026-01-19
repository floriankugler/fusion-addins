# Operation.tool Property

Parent Object: [Operation](Operation.md)  

## Description

Get or set the tool for this operation. The document's tool library will be updated accordingly. The tool instance returned is a copy and therefore is not referenced by the operation. To change the tool of the operation, the new tool must be assigned to the operation. Setting a tool will override the current preset and will fall back to the default preset of the new tool.

## Syntax

"operation_var" is a variable referencing an Operation object.  

```python
# Get the value of the property.
propertyValue = operation_var.tool

# Set the value of the property.
operation_var.tool = propertyValue
```

## Property Value

This is a read/write property whose value is a [Tool](Tool.md).

## Version

Introduced in version April 2023  

