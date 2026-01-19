# Machine Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a machine.

## Methods

| Name | Description |
|----|----|
| [classType](Machine_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [clearSimulationModel](Machine_clearSimulationModel.md) | Clears the simulation model from the machine. |
| [create](Machine_create.md) | Creates a machine from a "MachineInput" input object |
| [equivalentTo](Machine_equivalentTo.md) | Checks if the machine is equivalent to this one. |

## Properties

| Name | Description |
| --- | --- |
| [capabilities](Machine_capabilities.md) | Gets the capabilities of the machine. |
| [description](Machine_description.md) | Gets and sets the description of the machine. |
| [elements](Machine_elements.md) | Gets the list of elements that make up this machine. |
| [hasPost](Machine_hasPost.md) | Checks if the machine has a post. |
| [hasSimulationModel](Machine_hasSimulationModel.md) | Returns true if the machine has a simulation model attached. |
| [id](Machine_id.md) | Gets the unique identifier of the machine. Can be used for comparing machines within the document. |
| [isValid](Machine_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [model](Machine_model.md) | Gets and sets the model name of the machine. |
| [objectType](Machine_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [postURL](Machine_postURL.md) | Gets or sets the URL of the post assigned to the machine. |
| [vendor](Machine_vendor.md) | Gets and sets the vendor name of the machine. |

## Accessed From

[CAM.allMachines](CAM_allMachines.md), [Machine.create](Machine_create.md), [MachineLibrary.childMachines](MachineLibrary_childMachines.md), [MachineLibrary.machineAtURL](MachineLibrary_machineAtURL.md), [MachineQuery.execute](MachineQuery_execute.md), [NCProgram.machine](NCProgram_machine.md), [PrintSettingQuery.machine](PrintSettingQuery_machine.md), [Setup.machine](Setup_machine.md), [SetupInput.machine](SetupInput_machine.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |

## Version

Introduced in version April 2023  

