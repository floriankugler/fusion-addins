# MachineElements.itemsByType Method

Parent Object: [MachineElements](MachineElements.md)  

## Description

Gets the element of specified type.

## Syntax

"machineElements_var" is a variable referencing a [MachineElements](MachineElements.md) object.

```python
returnValue = machineElements_var.itemsByType(typeId)
```

## Return Value

| Type | Description |
|----|----|
| [MachineElement](MachineElement.md)\[\] | Returns a list of elements filtered to the specified type or an empty array if there is no match with the specified typeId. |

## Parameters

| Name | Type | Description |
|----|----|----|
| typeId | string | Element typeId to filter. See staticTypeId for the desired element type. |

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |

## Version

Introduced in version April 2023  

