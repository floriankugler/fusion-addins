# NCProgram.filteredOperations Property

Parent Object: [NCProgram](NCProgram.md)  

## Description

Gets all valid operations derived from the operations property. The list is ordered with respect to the nc_program_oderByTool parameter and considers the number of instances in a setup.

## Syntax

"nCProgram_var" is a variable referencing a NCProgram object.  

```python
# Get the value of the property.
propertyValue = nCProgram_var.filteredOperations
```

## Property Value

This is a read only property whose value is an array of type [OperationBase](OperationBase.md).

## Version

Introduced in version April 2023  

