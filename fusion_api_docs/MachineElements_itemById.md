# MachineElements.itemById Method

Parent Object: [MachineElements](MachineElements.md)  

## Description

Gets an element of a specific type by ID.

## Syntax

"machineElements_var" is a variable referencing a [MachineElements](MachineElements.md) object.

```python
returnValue = machineElements_var.itemById(typeId, elementId)
```

## Return Value

| Type | Description |
|----|----|
| [MachineElement](MachineElement.md) | Returns an element of the desired type with the specified ID or null in the case where no match is found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| typeId | string | Element typeId to filter. See staticTypeId for the desired element type. |
| elementId | string | Element ID to select. |

## Version

Introduced in version April 2023  

