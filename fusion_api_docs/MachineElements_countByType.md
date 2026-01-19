# MachineElements.countByType Method

Parent Object: [MachineElements](MachineElements.md)  

## Description

Number of elements of specified type.

## Syntax

"machineElements_var" is a variable referencing a [MachineElements](MachineElements.md) object.

```python
returnValue = machineElements_var.countByType(typeId)
```

## Return Value

| Type | Description |
|----|----|
| uinteger | Returns the number of elements of the requested type. Returns zero if no elements match the specified type ID. |

## Parameters

| Name | Type | Description |
|----|----|----|
| typeId | string | Element typeId to filter. See staticTypeId for the desired element type. |

## Version

Introduced in version April 2023  

