# CreateFromCAMTemplateInput.camTemplate Property

Parent Object: [CreateFromCAMTemplateInput](CreateFromCAMTemplateInput.md)  

## Description

Gets and sets the template to be instantiated.

## Syntax

"createFromCAMTemplateInput_var" is a variable referencing a CreateFromCAMTemplateInput object.  

```python
# Get the value of the property.
propertyValue = createFromCAMTemplateInput_var.camTemplate

# Set the value of the property.
createFromCAMTemplateInput_var.camTemplate = propertyValue
```

## Property Value

This is a read/write property whose value is a [CAMTemplate](CAMTemplate.md).

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |

## Version

Introduced in version October 2023  

