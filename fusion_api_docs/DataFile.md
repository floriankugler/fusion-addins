# DataFile Object

Derived from: [Base](Base.md) Object  

## Description

A data file in a data folder.

## Methods

| Name | Description |
| --- | --- |
| [classType](DataFile_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [copy](DataFile_copy.md) | Copies this DataFile to the specified folder. |
| [copyWithInput](DataFile_copyWithInput.md) | Executes the copy using the information defined by the provided CopyFileInput. |
| [createCopyDesignFileInput](DataFile_createCopyDesignFileInput.md) | Creates a new CopyDesignFileInput object that is used to create a copy of a DataFile that represents a Fusion design. You set options on the CopyDesignFileInput object to define the behavior of the copy and call the copyWithInput method passing in the input object to create the copy. |
| [createCopyFileInput](DataFile_createCopyFileInput.md) | Creates a new CopyFileInput object that is used to create a copy of any DataFile. |
| [createDataVersion](DataFile_createDataVersion.md) | Creates a version of this DataFile at tip. |
| [createMilestone](DataFile_createMilestone.md) | Makes the version this DataFile represents a milestone. |
| [deleteMe](DataFile_deleteMe.md) | Deletes this DataFile. This can fail if this file is referenced by another file or is currently open. |
| [download](DataFile_download.md) | Performs a synchronous or asynchronous download of this DataFile. Only DataFiles that represent non-Fusion data can be downloaded. For example, this will work for TXT or XLS files but will fail for F3D files. When using this in its synchronous mode, Fusion is frozen during the download and the call will not return until the download is complete or has failed. When using this in its asynchronous mode, calling this method will start the download process and the call return before the download is complete. The event on the provided handler will be called notifying you when the download is complete. |
| [move](DataFile_move.md) | Moves this DataFile to the specified folder. |
| [promote](DataFile_promote.md) | Promotes this version to be the latest version. If this is the latest version, nothing happens. |
| [refresh](DataFile_refresh.md) | Refreshes the data associated with a DataFile object to be up to date with the associated cloud data. The DataFile returned by the API reflects the local representation of the DataFile as used by the Data Panel. This is method is only useful in very limited cases and should rarely be used. In most cases the local representation will match the actual data on the cloud. In rare occasions where Fusion was off-line while the cloud processing of DataFile is completed or the DataFile is not in the folder shown in the Data Panel. Getting a DataFileFolder contents forces an update of the local data for all of the data files it contains so they will all be up to date. |

## Properties

| Name | Description |
| --- | --- |
| [childReferences](DataFile_childReferences.md) | Returns a collection of DataFiles that are the children (referenced designs) this datafile references. |
| [configurationRowId](DataFile_configurationRowId.md) | Returns the ID of the row that defines this configuration. Use the isCongiguration property to determine if this Design is a configuration or not. If this is not a configuration, this property returns an empty string. |
| [configurationTable](DataFile_configurationTable.md) | If this file is a configured design or a configuration, this property returns the associated ConfigTable object. If this is not a configured design or configuration, this property returns null. This property is typed as core.Base because the adsk.core library does not reference the fusion library where the ConfigurationTable object is defined. At runtime, this property will return a ConfigurationTable object. |
| [createdBy](DataFile_createdBy.md) | Returns the User that created this data file. |
| [dataObject](DataFile_dataObject.md) | Starts the process to get the raw binary data associated with this DataFile. Because the data exists on the cloud, a DataObjectFuture is returned that you can use to monitor the state of downloading the data and then getting the raw data once it is available. Only DataFiles that represent non-Fusion data can accessed. For example, this will work for TXT or XLS files but will fail for F3D files. |
| [dateCreated](DataFile_dateCreated.md) | Returns the date when this data file was created as UNIX epoch time. UNIX epoch time is the number of seconds since January 1, 1970 (midnight UTC/GMT). In Python you can import the standard time module to work with UNIX epoch time. In C++ you can use functions in time.h and std::chrono to work with UNIX epoch time. |
| [dateModified](DataFile_dateModified.md) | Returns the date when this data file was modified. Most changes to a file result in a new version which means a new DataFile is created and will have a new creation date. There are a few changes, like rename, that modify a DataFile without creating a new version and the date of that change is returned by this property. The date is returned as UNIX epoch time, which is the number of seconds since January 1, 1970 (midnight UTC/GMT). In Python you can import the standard time module to work with UNIX epoch time. In C++ you can use functions in time.h and std::chrono to work with UNIX epoch time. |
| [description](DataFile_description.md) | Gets and sets the description information associated with this item. |
| [fileExtension](DataFile_fileExtension.md) | Gets the file extension for this data file. The file type can be inferred from this. |
| [fusionWebURL](DataFile_fusionWebURL.md) | Returns a URL that can be used to access the Fusion Web interface for this file within a browser. The person using the URL must have an Autodesk account and have authority to access the hub this file is owned by. You can also use this URL to directly open the file in Fusion using the Fusion protocol handler as discussed in the [Opening Files from a Web Page](OpeningFilesFromWebPage_UM.md) topic in the API user manual. |
| [hasChildReferences](DataFile_hasChildReferences.md) | Gets if this datafile has children, (i.e. a Fusion Design containing referenced components). |
| [hasOutofDateChildReferences](DataFile_hasOutofDateChildReferences.md) | Gets if this datafile has Children (referenced components) that are out of date (not the latest version). |
| [hasParentReferences](DataFile_hasParentReferences.md) | Gets if this datafile has parents, (i.e. this is a child being referenced in another Fusion design). |
| [id](DataFile_id.md) | Returns the unique ID for this DataFile. This is the same id used in the APS Data Management API for an Item and is in the unencoded form and will look similar to this: "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w" |
| [inUseBy](DataFile_inUseBy.md) | Returns the array of users that are currently using (have open for edit) this data file. |
| [isComplete](DataFile_isComplete.md) | Returns if the DataFile is fully processed. This is especially useful when a new file is being saved or uploaded. The initial call to save or upload the file returns when the process has started but processing continues on the cloud. This property will return true when all of the processing has been completed and all information related to the Datafile is now available. |
| [isConfiguration](DataFile_isConfiguration.md) | Gets if this file is a configuration of a configuration table. If this returns true, the configurationRowId can be used to get the row used to define this configuration. Also, when this is true, the design is essentially read-only and edits are either blocked from taking place or cannot be saved. |
| [isConfiguredDesign](DataFile_isConfiguredDesign.md) | Gets if this file represents a configured design. This is a design where a configuration table is defined. Use the configurationTable property to get the associated table. |
| [isInUse](DataFile_isInUse.md) | Gets if this DataFile is currently in use (opened for edit) by any other user. |
| [isMilestone](DataFile_isMilestone.md) | Returns if the version this Datafile represents is a milestone. Returns true if it is a milestone. |
| [isReadOnly](DataFile_isReadOnly.md) | Gets if this file is currently read-only or not. A file can be read-only for various reasons. For example, if you are running with a "Fusion for Personal Use license" and have not designate the file to be editable or if someone else is editing the file. |
| [isValid](DataFile_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [lastUpdatedBy](DataFile_lastUpdatedBy.md) | Returns the User that last updated this data file |
| [latestVersion](DataFile_latestVersion.md) | Returns the latest version of the DataFile. It can return a reference to the same DataFile is this DataFile is the latest version. |
| [latestVersionNumber](DataFile_latestVersionNumber.md) | Gets the latest version number for this DataFile. |
| [milestone](DataFile_milestone.md) | If the version this DataFile represents is a milestone, a Milestone object will be returned. If it's not a milestone, null is returned. |
| [milestones](DataFile_milestones.md) | Returns a collection of Milestones associated with all versions of this DataFile. |
| [name](DataFile_name.md) | Gets and sets the displayed name of this item. |
| [objectType](DataFile_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFolder](DataFile_parentFolder.md) | Returns the parent folder this item is contained within. |
| [parentProject](DataFile_parentProject.md) | Returns the parent project that this item is in. |
| [parentReferences](DataFile_parentReferences.md) | Returns a collection DataFiles collection that are the parents (designs that reference) this datafile. |
| [publicLink](DataFile_publicLink.md) | **RETIRED** Returns a short URL of this data file which can be shared with others. |
| [sharedLink](DataFile_sharedLink.md) | Returns the SharedLink object associated with this DataFile. You can use the SharedLink object to enable a shared link and set its behavior and to get the shared link URL. |
| [thumbnail](DataFile_thumbnail.md) | Starts the process to get the thumbnail image data associated with this DataFile. Because the data exists on the cloud, a DataObjectFuture is returned that you can use to monitor the state of downloading the thumbnail and then getting the image once it is available. The data returned is a 256x256 PNG image. For cases where the DataFile does not have an associated thumbnail, the dataObject property of the returned DataObjectFuture will return null and the state property will return 'FailedFutureState'. |
| [versionId](DataFile_versionId.md) | Returns the version ID for this DataFile. This is the same id used in the APS Data Management API for an Item and is in the unencoded form and will look similar to this: "urn:adsk.wipqa:fs.file:vf.W3syIw1lQAW-5vWObMdYnA?version=2" |
| [versionNumber](DataFile_versionNumber.md) | Gets the version number of this DataFile. |
| [versions](DataFile_versions.md) | Gets the other version of this item. |

## Accessed From

[CloudFileDialog.dataFile](CloudFileDialog_dataFile.md), [CloudFileDialog.dataFiles](CloudFileDialog_dataFiles.md), [ConfigurationReplaceDesign.dataFile](ConfigurationReplaceDesign_dataFile.md), [Data.findFileById](Data_findFileById.md), [DataEventArgs.file](DataEventArgs_file.md), [DataFile.copy](DataFile_copy.md), [DataFile.latestVersion](DataFile_latestVersion.md), [DataFileFuture.dataFile](DataFileFuture_dataFile.md), [DataFiles.asArray](DataFiles_asArray.md), [DataFiles.item](DataFiles_item.md), [DataFiles.itemById](DataFiles_itemById.md), [DesignDataFile.copy](DesignDataFile_copy.htm), [DesignDataFile.latestVersion](DesignDataFile_latestVersion.htm), [Document.dataFile](Document_dataFile.md), [DocumentReference.dataFile](DocumentReference_dataFile.md), [DrawingDocument.dataFile](DrawingDocument_dataFile.md), [FusionDocument.dataFile](FusionDocument_dataFile.md), [Milestone.version](Milestone_version.md), [Occurrence.configuredDataFile](Occurrence_configuredDataFile.md), [PersonalUseLimits.editableFiles](PersonalUseLimits_editableFiles.md)

## Samples

| Name | Description |
| --- | --- |
| [Avoid Machine Surface Settings API Sample](AvoidMachineSurfaceSettings_Sample.md) | This sample script demonstrates how to use Machine/Avoid/Gouge/Fixture functionality. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a curved surface with a through slot, a countersunk hole and a raised, circular and filleted upstand from the surface. The model is supported by two rectangular blocks, themselves mounted on a fixture plate. A setup is included with a single operation running a 3-axis diagonal raster over the model, supports and fixture. The operation machines the fixture, the supporting blocks, the upper surface of the upstand and the area within the slot and hole, something we would like to avoid. The script duplicates the original operation and then proceeds to create a series of MachineAvoidGroups. These are labelled as either Machine in the case of 2 cap surfaces for the slot and hole, Fixture for the fixture plate, Gouge for the supporting blocks and Avoid for the top face of the upstand. Additionally, both AxialOffset and RadialOffset can be specified for the Machine, Avoid and Fixture passes. |
| [Create Engravings Selection Sets API Sample](CreateEngravingsSelectionSets_Sample.md) | This sample script demonstrates how to find and machine engravings in the Z+ direction using pocket recognition. The script will first open an example model via its URN. Using pocket recognition, it will identify pockets that may be engravings based on their dimensions. We assume here that an engraving pocket is: Made with a flat bottom face and no fillet. A closed pocket. Have a Z height less than 2 mm We demonstrate creating selection sets in both design and manufacture workspaces and use one of the selection sets as an operation geometry selection input to generate an engraving operation. The engraving toolpath can be seen by expanding the setup and selecting the operation. |
| [Create Setups From Hole Recognition API Sample](CreateSetupsFromHoleRecognition_Sample.md) | This sample script demonstrates how to create a correctly oriented setup using Hole Recognition functionality. The Fusion Manufacturing Extension is required for Hole Recognition. The script starts by opening a sample model from the CAM Samples folder via its URN. The model comprises a 3 way coupling containing holes in various orientations and mounted on a fixture. A reference setup is created for the model using a simple stock mode and offsets. The Hole Recognition feature of the Fusion Manufacturing Extension creates 5 hole groups containing 11 holes between them. For each unique hole group vector captured, a new setup is created and its orientation transformed to match the vector. |
| [Set Vise Origin As Setup WCS Origin API Sample](SetViseOriginAsSetupWCSOrigin_Sample.md) | This sample script demonstrates how to define our setup WCS origin relative to our vise origin from either a component, a sketch point or a joint origin. The Work Coordinate System is a reference point set in our CAM workspace and on our machine. All machine coordinates are drawn from the WCS. This script demonstrates defining the WCS by each of 4 alternative methods: Setup by default with no origin defined. Setup using vise origin as WCS origin. Setup using a sketch point as WCS origin. Setup using a joint origin as WCS origin. |

## Version

Introduced in version January 2015  

