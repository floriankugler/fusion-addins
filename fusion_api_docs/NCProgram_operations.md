# NCProgram.operations Property

Parent Object: [NCProgram](NCProgram.md)  

## Description

Gets and sets the operations which will be included in the NC program. Valid input contains any number of operations, setups or folders. For setups and folders all child operations will be added. Operations will be post processed in setup order, with operations from the same setup grouped together. Setting the nc_program_orderByTool BooleanParameterValue on the parameters property to true will reorder operations across multiple setups to reduce the number of tool changes.

## Syntax

"nCProgram_var" is a variable referencing a NCProgram object.  

```python
# Get the value of the property.
propertyValue = nCProgram_var.operations

# Set the value of the property.
nCProgram_var.operations = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type [OperationBase](OperationBase.md).

## Version

Introduced in version April 2023  

