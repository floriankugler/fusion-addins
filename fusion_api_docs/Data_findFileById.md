# Data.findFileById Method

Parent Object: [Data](Data.md)  

## Description

Returns the DataFile identified by the input id. This can fail is there isn't a DataFile identified with the specified id or if the current user doesn't have privileges to access the file.

## Syntax

"data_var" is a variable referencing a [Data](Data.md) object.

```python
returnValue = data_var.findFileById(id)
```

## Return Value

| Type | Description |
|----|----|
| [DataFile](DataFile.md) | Returns the DataFile is one was found matching the input id or null if one was not found or you don't have privileges to access it. You can use the Application.getLastError method to determine the reason for the failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| id | string | The full id of the file will be something similar to that shown below. The version argument can be omitted which will result in getting the latest version. urn:adsk.wipprod:fs.file:vf.NazykCYLRWKZ5tpzJtEQ1A?version=3 This is also the same id that you'll obtain if you use the APS Data Management API. |

## Samples

| Name | Description |
| --- | --- |
| [Avoid Machine Surface Settings API Sample](AvoidMachineSurfaceSettings_Sample.md) | This sample script demonstrates how to use Machine/Avoid/Gouge/Fixture functionality. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a curved surface with a through slot, a countersunk hole and a raised, circular and filleted upstand from the surface. The model is supported by two rectangular blocks, themselves mounted on a fixture plate. A setup is included with a single operation running a 3-axis diagonal raster over the model, supports and fixture. The operation machines the fixture, the supporting blocks, the upper surface of the upstand and the area within the slot and hole, something we would like to avoid. The script duplicates the original operation and then proceeds to create a series of MachineAvoidGroups. These are labelled as either Machine in the case of 2 cap surfaces for the slot and hole, Fixture for the fixture plate, Gouge for the supporting blocks and Avoid for the top face of the upstand. Additionally, both AxialOffset and RadialOffset can be specified for the Machine, Avoid and Fixture passes. |
| [Create Engravings Selection Sets API Sample](CreateEngravingsSelectionSets_Sample.md) | This sample script demonstrates how to find and machine engravings in the Z+ direction using pocket recognition. The script will first open an example model via its URN. Using pocket recognition, it will identify pockets that may be engravings based on their dimensions. We assume here that an engraving pocket is: Made with a flat bottom face and no fillet. A closed pocket. Have a Z height less than 2 mm We demonstrate creating selection sets in both design and manufacture workspaces and use one of the selection sets as an operation geometry selection input to generate an engraving operation. The engraving toolpath can be seen by expanding the setup and selecting the operation. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version December 2020  

