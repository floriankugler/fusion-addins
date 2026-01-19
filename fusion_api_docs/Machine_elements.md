# Machine.elements Property

Parent Object: [Machine](Machine.md)  

## Description

Gets the list of elements that make up this machine.

## Syntax

"machine_var" is a variable referencing a Machine object.  

```python
# Get the value of the property.
propertyValue = machine_var.elements
```

## Property Value

This is a read only property whose value is a [MachineElements](MachineElements.md).

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |

## Version

Introduced in version April 2023  

