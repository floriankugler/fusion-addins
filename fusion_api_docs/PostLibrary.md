# PostLibrary Object

Derived from: [CAMLibrary](CAMLibrary.md) Object  

## Description

The PostLibrary provides access to post configurations. Using this object you can import post configurations and get existing post configurations using either a URL or query to find specific post configurations.

## Methods

| Name | Description |
|----|----|
| [childAssetURLs](PostLibrary_childAssetURLs.md) | Get all assets under given URL. |
| [childFolderURLs](PostLibrary_childFolderURLs.md) | Get all library folders under given URL. |
| [childPostConfigurations](PostLibrary_childPostConfigurations.md) | Get all posts by the given parent folder URL. Returns null, if the URL does not exist. |
| [classType](PostLibrary_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFolder](PostLibrary_createFolder.md) | Create a new folder in the library. Create the folder under given parent URL with given folder name. Add counting suffix, in case a folder with given name already exists. Throw an error if given URL does not point to a valid folder or the URL is read-only. Also throws an error if given folder name is empty. |
| [createQuery](PostLibrary_createQuery.md) | Creates a new PostConfigurationQuery that is used to query the library for post configurations matching the query. |
| [deleteAsset](PostLibrary_deleteAsset.md) | Delete asset by URL from the library. Throw an error if given URL does not point to a valid asset or the URL is read-only. |
| [deleteFolder](PostLibrary_deleteFolder.md) | Delete folder by URL from the library. Any content of the folder will also be deleted. Throw an error if given URL does not point to a valid folder or the URL is read-only. |
| [displayName](PostLibrary_displayName.md) | Get the localized display name for a given URL. The URL must point to a folder. |
| [doesPathExist](PostLibrary_doesPathExist.md) | Checks if the given URL points to an existing folder or asset in the library. |
| [importPostConfiguration](PostLibrary_importPostConfiguration.md) | Import a given post configuration at a specific location. The post configuration will be stored in the library. Throws an error, if the given URL is read-only. |
| [postConfigurationAtURL](PostLibrary_postConfigurationAtURL.md) | Get a specific post configuration by the given URL. Returns null, if the URL does not exist. |
| [urlByLocation](PostLibrary_urlByLocation.md) | Get the URL for a given LibraryLocations. |

## Properties

| Name | Description |
| --- | --- |
| [assetTypeName](PostLibrary_assetTypeName.md) | Get the name of the asset type which can be accessed by the library. |
| [isValid](PostLibrary_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PostLibrary_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMLibraryManager.postLibrary](CAMLibraryManager_postLibrary.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

