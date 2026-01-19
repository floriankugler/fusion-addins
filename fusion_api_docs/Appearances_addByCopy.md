# Appearances.addByCopy Method

Parent Object: [Appearances](Appearances.md)  

## Description

Add an Appearance to a Design by copying an existing Appearance from Favorites, a Library or from the appearances stored in the Design. This method currently only applies to the Appearances collection from a Design and cannot be used to copy an Appearance to a library.

## Syntax

"appearances_var" is a variable referencing an [Appearances](Appearances.md) object.

```python
returnValue = appearances_var.addByCopy(appearanceToCopy, name)
```

## Return Value

| Type | Description |
|----|----|
| [Appearance](Appearance.md) | Returns the newly created Appearance or null if the copy operation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| appearanceToCopy | [Appearance](Appearance.md) | The Appearance you want to copy. The Appearance to copy can be from Favorites, a Library or from the appearances stored in the Design. |
| name | string | The Appearance name to apply to the copy. |

## Samples

| Name | Description |
| --- | --- |
| [Avoid Machine Surface Settings API Sample](AvoidMachineSurfaceSettings_Sample.md) | This sample script demonstrates how to use Machine/Avoid/Gouge/Fixture functionality. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a curved surface with a through slot, a countersunk hole and a raised, circular and filleted upstand from the surface. The model is supported by two rectangular blocks, themselves mounted on a fixture plate. A setup is included with a single operation running a 3-axis diagonal raster over the model, supports and fixture. The operation machines the fixture, the supporting blocks, the upper surface of the upstand and the area within the slot and hole, something we would like to avoid. The script duplicates the original operation and then proceeds to create a series of MachineAvoidGroups. These are labelled as either Machine in the case of 2 cap surfaces for the slot and hole, Fixture for the fixture plate, Gouge for the supporting blocks and Avoid for the top face of the upstand. Additionally, both AxialOffset and RadialOffset can be specified for the Machine, Avoid and Fixture passes. |
| [Create Engravings Selection Sets API Sample](CreateEngravingsSelectionSets_Sample.md) | This sample script demonstrates how to find and machine engravings in the Z+ direction using pocket recognition. The script will first open an example model via its URN. Using pocket recognition, it will identify pockets that may be engravings based on their dimensions. We assume here that an engraving pocket is: Made with a flat bottom face and no fillet. A closed pocket. Have a Z height less than 2 mm We demonstrate creating selection sets in both design and manufacture workspaces and use one of the selection sets as an operation geometry selection input to generate an engraving operation. The engraving toolpath can be seen by expanding the setup and selecting the operation. |
| [Material API Sample](MaterialSample_Sample.md) | Demonstrates using materials and appearance using the API. To use the sample, create a new Python or C++ script and copy and paste this code, replacing the default code. The sample also used an external appearance library which you can get [here](../ExtraFiles/APISampleMaterialLibrary2.adsklib). Copy that to any location on your computer and edit the path in the script. When running the script, have a design open that contains a body in the root component. |

## Version

Introduced in version January 2016  

