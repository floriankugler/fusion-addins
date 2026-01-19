# MachinePart.parent Property

Parent Object: [MachinePart](MachinePart.md)  

## Description

Get or set the parent of this part. Returns null if this part is a root part. Setting the parent will add this part to the end of the parent's children collection. Setting the parent will throw an error if the new parent is this part or a child of this part.

## Syntax

"machinePart_var" is a variable referencing a MachinePart object.  

```python
# Get the value of the property.
propertyValue = machinePart_var.parent

# Set the value of the property.
machinePart_var.parent = propertyValue
```

## Property Value

This is a read/write property whose value is a [MachinePart](MachinePart.md).

## Version

Introduced in version April 2023  

