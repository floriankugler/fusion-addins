# NCProgram.machine Property

Parent Object: [NCProgram](NCProgram.md)  

## Description

Gets and sets the machine of this NC program. When a machine is set, "use machine configuration" is automatically set to true. If this machine has a default post assigned, this post will be set for the NC program as well.

## Syntax

"nCProgram_var" is a variable referencing a NCProgram object.  

```python
# Get the value of the property.
propertyValue = nCProgram_var.machine

# Set the value of the property.
nCProgram_var.machine = propertyValue
```

## Property Value

This is a read/write property whose value is a [Machine](Machine.md).

## Version

Introduced in version April 2023  

