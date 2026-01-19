# MachineElements.defaultItemByType Method

Parent Object: [MachineElements](MachineElements.md)  

## Description

Returns the default item of the given type. In most cases this will be the element with an element ID of "default".

## Syntax

"machineElements_var" is a variable referencing a [MachineElements](MachineElements.md) object.

```python
returnValue = machineElements_var.defaultItemByType(typeId)
```

## Return Value

| Type | Description |
|----|----|
| [MachineElement](MachineElement.md) | Returns the specified Element or null if no matching type ID is found. |

## Parameters

| Name | Type | Description |
|----|----|----|
| typeId | string | Element typeId to get the default for. See staticTypeId for the desired element type. |

## Version

Introduced in version April 2023  

