# CAM.setups Property

Parent Object: [CAM](CAM.md)  

## Description

Returns the Setups collection that provides access to existing setups.

## Syntax

"cAM_var" is a variable referencing a CAM object.  

```python
# Get the value of the property.
propertyValue = cAM_var.setups
```

## Property Value

This is a read only property whose value is a [Setups](Setups.md).

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [CAM Parameter Modification API Sample](CAMParameterChange_Sample_Sample.md) | Demonstrates changing parameters of existing toolpaths. |
| [Generate Setup Sheets API Sample](GenerateSetupSheets_Sample_Sample.md) | Demonstrates generating the setup sheets for an existing toolpath.. |
| [Generate Toolpaths API Sample](GenerateToolpaths_Sample_Sample.md) | Demonstrates generating the toolpaths in the active document. |
| [Create CAM Operation From Template API Sample](New_Operation_Sample_Sample.md) | Demonstrates adding a new toolpath into the document using an existing CAM template. You can view the template [here](../ExtraFiles/face.f3dhsm-template), although it will be loaded automatically. Run the sample script within any Fusion project containing at least one setup. A new facing operation will be created at the end of each setup discovered. |
| [Post Toolpaths API Sample](PostToolpaths_Sample_Sample.md) | Demonstrates posting toolpaths in the active document. |

## Version

Introduced in version January 2016  

