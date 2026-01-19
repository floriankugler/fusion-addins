# CAMLibrary Object

Derived from: [Base](Base.md) Object  

## Description

The CAMLibrary is the base-class for all other asset-specific libraries.

## Methods

| Name | Description |
|----|----|
| [childAssetURLs](CAMLibrary_childAssetURLs.md) | Get all assets under given URL. |
| [childFolderURLs](CAMLibrary_childFolderURLs.md) | Get all library folders under given URL. |
| [classType](CAMLibrary_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFolder](CAMLibrary_createFolder.md) | Create a new folder in the library. Create the folder under given parent URL with given folder name. Add counting suffix, in case a folder with given name already exists. Throw an error if given URL does not point to a valid folder or the URL is read-only. Also throws an error if given folder name is empty. |
| [deleteAsset](CAMLibrary_deleteAsset.md) | Delete asset by URL from the library. Throw an error if given URL does not point to a valid asset or the URL is read-only. |
| [deleteFolder](CAMLibrary_deleteFolder.md) | Delete folder by URL from the library. Any content of the folder will also be deleted. Throw an error if given URL does not point to a valid folder or the URL is read-only. |
| [displayName](CAMLibrary_displayName.md) | Get the localized display name for a given URL. The URL must point to a folder. |
| [doesPathExist](CAMLibrary_doesPathExist.md) | Checks if the given URL points to an existing folder or asset in the library. |
| [urlByLocation](CAMLibrary_urlByLocation.md) | Get the URL for a given LibraryLocations. |

## Properties

| Name | Description |
| --- | --- |
| [assetTypeName](CAMLibrary_assetTypeName.md) | Get the name of the asset type which can be accessed by the library. |
| [isValid](CAMLibrary_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](CAMLibrary_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Derived Classes

[CAMTemplateLibrary](CAMTemplateLibrary.md), [MachineLibrary](MachineLibrary.md), [PostLibrary](PostLibrary.md), [PrintSettingLibrary](PrintSettingLibrary.md), [StockMaterialLibrary](StockMaterialLibrary.md), [ToolLibraries](ToolLibraries.md)

## Version

Introduced in version April 2023  

