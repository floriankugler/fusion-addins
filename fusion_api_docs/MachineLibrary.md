# MachineLibrary Object

Derived from: [CAMLibrary](CAMLibrary.md) Object  

## Description

The MachineLibrary provides access to machines. Using this object you can import machines and get existing machines using either URL or query to find specific Machines.

## Methods

| Name | Description |
|----|----|
| [childAssetURLs](MachineLibrary_childAssetURLs.md) | Get all assets under given URL. |
| [childFolderURLs](MachineLibrary_childFolderURLs.md) | Get all library folders under given URL. |
| [childMachines](MachineLibrary_childMachines.md) | Get all machines by the given parent folder URL. Returns null, if the URL does not exist. |
| [classType](MachineLibrary_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFolder](MachineLibrary_createFolder.md) | Create a new folder in the library. Create the folder under given parent URL with given folder name. Add counting suffix, in case a folder with given name already exists. Throw an error if given URL does not point to a valid folder or the URL is read-only. Also throws an error if given folder name is empty. |
| [createQuery](MachineLibrary_createQuery.md) | Creates a new MachineQuery that is used to query the library for machines matching the query. |
| [deleteAsset](MachineLibrary_deleteAsset.md) | Delete asset by URL from the library. Throw an error if given URL does not point to a valid asset or the URL is read-only. |
| [deleteFolder](MachineLibrary_deleteFolder.md) | Delete folder by URL from the library. Any content of the folder will also be deleted. Throw an error if given URL does not point to a valid folder or the URL is read-only. |
| [displayName](MachineLibrary_displayName.md) | Get the localized display name for a given URL. The URL must point to a folder. |
| [doesPathExist](MachineLibrary_doesPathExist.md) | Checks if the given URL points to an existing folder or asset in the library. |
| [importMachine](MachineLibrary_importMachine.md) | Import a given machine at a specific location. The machine will be stored in the library. Throws an error, if the given URL is read-only. |
| [machineAtURL](MachineLibrary_machineAtURL.md) | Get a specific machine by the given URL. Returns null, if the URL does not exist. |
| [updateMachine](MachineLibrary_updateMachine.md) | Update a machine in the library. The library overrides the URL by given machine. Throws an error if the URL does not already point to an existing machine. |
| [urlByLocation](MachineLibrary_urlByLocation.md) | Get the URL for a given LibraryLocations. |

## Properties

| Name | Description |
| --- | --- |
| [assetTypeName](MachineLibrary_assetTypeName.md) | Get the name of the asset type which can be accessed by the library. |
| [isValid](MachineLibrary_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](MachineLibrary_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMLibraryManager.machineLibrary](CAMLibraryManager_machineLibrary.md)

## Samples

| Name | Description |
| --- | --- |
| [Additive Manufacturing FFF API Sample](AdditiveFFFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive FFF manufacturing setup and generate a toolpath. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select an FFF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected FFF machine. This script will also create support structures, if required, based on the orientation of each component. Finally, the script generates the toolpath for the active setup and lets the user choose if they wish to post process the resulting toolpath or if they want to simulate it. |
| [Additive Manufacturing MJF API Sample](AdditiveMJFManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive MJF manufacturing setup and arrange components within the build volume of a 3D printer. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive Arrange using that manufacturing model as an input. The setup will select an MJF 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically arranged within the build volume of the selected MJF machine. |
| [Additive Manufacturing SLA API Sample](AdditiveSLAManufacturingSample_Sample.md) | Demonstrates how to automate the creation of an additive SLA manufacturing setup. To run the sample script, have a design with one or more components open in Fusion’s DESIGN workspace. This script will switch the UI from the DESIGN workspace to the MANUFACTURE workspace, create a new Manufacturing Model, and create an Additive setup using that manufacturing model as an input. The setup will select a SLA 3D printer from Fusion’s machine library and a print setting from the print setting library. All components in the Manufacturing model will be automatically oriented and arranged within the build area of the selected SLA machine. This script will also create support structures, based on the orientation of each component. The support and orientation operations are created from a template. The script further demonstrates how to wrap script code into a command such that only one undo entry is created for the entire script instead of one entry per internal action. |

## Version

Introduced in version April 2023  

