# Setup.createFromCAMTemplate2 Method

Parent Object: [Setup](Setup.md)  

## Description

Create new operations, folders, or patterns from the specified CAMTemplate. They are added to the end of the parent setup.

## Syntax

"setup_var" is a variable referencing a [Setup](Setup.md) object.

```python
returnValue = setup_var.createFromCAMTemplate2(input)
```

## Return Value

| Type | Description |
|----|----|
| [OperationBase](OperationBase.md)\[\] | Returns an array containing all of the operations, folders and patterns created from the template. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CreateFromCAMTemplateInput](CreateFromCAMTemplateInput.md) | Input object that contains the template to create from and the generation mode. |

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |
| [Create CAM Operation From Template API Sample](New_Operation_Sample_Sample.md) | Demonstrates adding a new toolpath into the document using an existing CAM template. You can view the template [here](../ExtraFiles/face.f3dhsm-template), although it will be loaded automatically. Run the sample script within any Fusion project containing at least one setup. A new facing operation will be created at the end of each setup discovered. |

## Version

Introduced in version October 2023  

