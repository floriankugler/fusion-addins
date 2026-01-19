# Data Object

Derived from: [Base](Base.md) Object  

## Description

The Data class provides access to data files

## Methods

| Name | Description |
|----|----|
| [classType](Data_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [findFileById](Data_findFileById.md) | Returns the DataFile identified by the input id. This can fail is there isn't a DataFile identified with the specified id or if the current user doesn't have privileges to access the file. |
| [findFolderById](Data_findFolderById.md) | Returns the DataFolder identified by the input id. This can fail if there isn't a DataFolder identified with the specified id or if the current user doesn't have privileges to access the folder. |
| [refreshDataPanel](Data_refreshDataPanel.md) | Refreshes the contents of the data panel to ensure what is displayed reflects the latest state. |

## Properties

| Name | Description |
| --- | --- |
| [activeFolder](Data_activeFolder.md) | Gets the active DataFolder as seen in the Fusion Data Panel. |
| [activeHub](Data_activeHub.md) | Gets the active DataHub. |
| [activeProject](Data_activeProject.md) | Gets and sets the active DataProject. This is the project currently displayed in the Fusion Data Panel. |
| [dataHubs](Data_dataHubs.md) | Returns a collection of accessible hubs for the current user. A DataHub represents an A360 Team or Personal hub. |
| [dataProjects](Data_dataProjects.md) | Gets the collection of DataProjects associated with the active Hub. |
| [isDataPanelVisible](Data_isDataPanelVisible.md) | Gets and sets if the data panel is visible within Fusion. |
| [isValid](Data_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](Data_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [personalUseLimits](Data_personalUseLimits.md) | If the user is running with a "Fusion for Personal Use license", this property will return a peronalUseLimits object which provides information about file limits associated with the license. If the user is running with any other license type, this property will return null. |

## Accessed From

[Application.data](Application_data.md)

## Samples

| Name | Description |
| --- | --- |
| [Avoid Machine Surface Settings API Sample](AvoidMachineSurfaceSettings_Sample.md) | This sample script demonstrates how to use Machine/Avoid/Gouge/Fixture functionality. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a curved surface with a through slot, a countersunk hole and a raised, circular and filleted upstand from the surface. The model is supported by two rectangular blocks, themselves mounted on a fixture plate. A setup is included with a single operation running a 3-axis diagonal raster over the model, supports and fixture. The operation machines the fixture, the supporting blocks, the upper surface of the upstand and the area within the slot and hole, something we would like to avoid. The script duplicates the original operation and then proceeds to create a series of MachineAvoidGroups. These are labelled as either Machine in the case of 2 cap surfaces for the slot and hole, Fixture for the fixture plate, Gouge for the supporting blocks and Avoid for the top face of the upstand. Additionally, both AxialOffset and RadialOffset can be specified for the Machine, Avoid and Fixture passes. |
| [Create Engravings Selection Sets API Sample](CreateEngravingsSelectionSets_Sample.md) | This sample script demonstrates how to find and machine engravings in the Z+ direction using pocket recognition. The script will first open an example model via its URN. Using pocket recognition, it will identify pockets that may be engravings based on their dimensions. We assume here that an engraving pocket is: Made with a flat bottom face and no fillet. A closed pocket. Have a Z height less than 2 mm We demonstrate creating selection sets in both design and manufacture workspaces and use one of the selection sets as an operation geometry selection input to generate an engraving operation. The engraving toolpath can be seen by expanding the setup and selecting the operation. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version January 2015  

