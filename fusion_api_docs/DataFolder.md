# DataFolder Object

Derived from: [Base](Base.md) Object  

## Description

A data folder that contains a collection of data items.

## Methods

| Name | Description |
|----|----|
| [classType](DataFolder_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [deleteMe](DataFolder_deleteMe.md) | Deletes this folder item. |
| [uploadAssembly](DataFolder_uploadAssembly.md) | Uploads a set of files that represent an assembly There should only be a single top-level assembly file but there can be any number of other files that represent sub-assemblies. |
| [uploadFile](DataFolder_uploadFile.md) | Uploads a single file to this directory. |

## Properties

| Name | Description |
| --- | --- |
| [dataFiles](DataFolder_dataFiles.md) | Returns a collection containing all of the items within this folder, excluding folders. Use the dataFolders property to get the folders. |
| [dataFolders](DataFolder_dataFolders.md) | Returns a collection containing all of the folders within this folder. |
| [id](DataFolder_id.md) | Returns the unique ID for this folder. This is the same id used in the APS Data Management API. |
| [isRoot](DataFolder_isRoot.md) | Indicates if this folder is the root folder within the parent project. |
| [isValid](DataFolder_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [name](DataFolder_name.md) | Gets and sets the displayed name of this folder. |
| [objectType](DataFolder_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parentFolder](DataFolder_parentFolder.md) | Returns the parent folder this folder is contained within. Returns null if this is the project's root folder. |
| [parentProject](DataFolder_parentProject.md) | Returns the parent project that owns this folder. |

## Accessed From

[CloudFileDialog.dataFolder](CloudFileDialog_dataFolder.md), [CopyDesignFileInput.targetFolder](CopyDesignFileInput_targetFolder.md), [CopyFileInput.targetFolder](CopyFileInput_targetFolder.md), [Data.activeFolder](Data_activeFolder.md), [Data.findFolderById](Data_findFolderById.md), [DataFile.parentFolder](DataFile_parentFolder.md), [DataFolder.parentFolder](DataFolder_parentFolder.md), [DataFolders.add](DataFolders_add.md), [DataFolders.asArray](DataFolders_asArray.md), [DataFolders.item](DataFolders_item.md), [DataFolders.itemById](DataFolders_itemById.md), [DataFolders.itemByName](DataFolders_itemByName.md), [DataProject.rootFolder](DataProject_rootFolder.md), [DesignDataFile.parentFolder](DesignDataFile_parentFolder.htm), [NCProgram.fusionHubFolder](NCProgram_fusionHubFolder.md)

## Version

Introduced in version January 2015  

