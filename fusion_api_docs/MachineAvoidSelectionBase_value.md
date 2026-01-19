# MachineAvoidSelectionBase.value Property

Parent Object: [MachineAvoidSelectionBase](MachineAvoidSelectionBase.md)  

## Description

Returns the resulting value of the selection. In general, this returns the input selection, but child classes can override the return value if needed. Refer to the child classes comments for further details. The collection may contain duplicates. For OperationInputs, the return value may not be the same as for Operations, as additional geometry selected by child classes is not evaluated for OperationInputs.

## Syntax

"machineAvoidSelectionBase_var" is a variable referencing a MachineAvoidSelectionBase object.  

```python
# Get the value of the property.
propertyValue = machineAvoidSelectionBase_var.value
```

## Property Value

This is a read only property whose value is an array of type [Base](Base.md).

## Version

Introduced in version September 2024  

