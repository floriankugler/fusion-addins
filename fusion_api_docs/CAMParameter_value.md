# CAMParameter.value Property

Parent Object: [CAMParameter](CAMParameter.md)  

## Description

Returns an object that allows you to get and set the value associated with the parameter.

## Remarks

Within CAM operations, floating point values (via FloatParameterValue) are returned and set using a standardized set of "internal" units, rather than using the document units. The units used depend on the type of parameter. For reference, the units used are:

- Length - centimeters (cm)
- Angle - radians (rad)
- Linear velocity - millimeters/minute (mm/min)
- Rotational velocity - revolutions per minute (rpm)
- Time - seconds (s)
- Weight - kilograms (kg)
- Power - Watts (W)
- Flow rate - liters/minute (l/min)
- Area - square centimeters (cm²)
- Volume - cubic centimeters (cm³)
- Temperature - degrees Celsius (C)

## Syntax

"cAMParameter_var" is a variable referencing a CAMParameter object.  

```python
# Get the value of the property.
propertyValue = cAMParameter_var.value
```

## Property Value

This is a read only property whose value is a [ParameterValue](ParameterValue.md).

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |

## Version

Introduced in version November 2021  

