
Derived from: [CAMLibrary](CAMLibrary.md) Object  

This functionality is provided as a preview of intended future API capabilities. You are encouraged to use it and report any problems or suggestions using the [Fusion API and Scripts](https://forums.autodesk.com/t5/fusion-360-api-and-scripts/bd-p/22) forum.  

Because this is a preview of future functionality, there is the possibility that it will change, which will possibly break any existing programs that use this functionality. Because of that, you should never deliver any programs that use any preview capabilities. For a distributed program, you should wait until it has moved from preview to released state.

## Description

The StockMaterialLibraries object provides utilities to access, import and update stock material by URL.

## Methods

| Name | Description |
|----|----|
| [childAssetURLs](StockMaterialLibrary_childAssetURLs.md) | Get all assets under given URL. |
| [childFolderURLs](StockMaterialLibrary_childFolderURLs.md) | Get all library folders under given URL. |
| [childStockMaterials](StockMaterialLibrary_childStockMaterials.md) | Get all stockMaterials by the given parent folder URL. Returns null, if the URL does not exist. |
| [classType](StockMaterialLibrary_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createFolder](StockMaterialLibrary_createFolder.md) | Create a new folder in the library. Create the folder under given parent URL with given folder name. Add counting suffix, in case a folder with given name already exists. Throw an error if given URL does not point to a valid folder or the URL is read-only. Also throws an error if given folder name is empty. |
| [deleteAsset](StockMaterialLibrary_deleteAsset.md) | Delete asset by URL from the library. Throw an error if given URL does not point to a valid asset or the URL is read-only. |
| [deleteFolder](StockMaterialLibrary_deleteFolder.md) | Delete folder by URL from the library. Any content of the folder will also be deleted. Throw an error if given URL does not point to a valid folder or the URL is read-only. |
| [displayName](StockMaterialLibrary_displayName.md) | Get the localized display name for a given URL. The URL must point to a folder. |
| [doesPathExist](StockMaterialLibrary_doesPathExist.md) | Checks if the given URL points to an existing folder or asset in the library. |
| [importStockMaterial](StockMaterialLibrary_importStockMaterial.md) | Import a given stockMaterial at a specific location. The stockMaterial will be stored in the library. Throws an error, if the given URL is read-only. |
| [stockMaterialAtURL](StockMaterialLibrary_stockMaterialAtURL.md) | Get a specific stockMaterial by the given URL. Returns null, if the URL does not exist. |
| [updateStockMaterial](StockMaterialLibrary_updateStockMaterial.md) | Update a stockMaterial in the library. The library overrides the URL by given stockMaterial. Throws an error if the URL does not already point to an existing stockMaterial. |
| [urlByLocation](StockMaterialLibrary_urlByLocation.md) | Get the URL for a given LibraryLocations. |

## Properties

| Name | Description |
| --- | --- |
| [assetTypeName](StockMaterialLibrary_assetTypeName.md) | Get the name of the asset type which can be accessed by the library. |
| [isValid](StockMaterialLibrary_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](StockMaterialLibrary_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[CAMLibraryManager.stockMaterialLibrary](CAMLibraryManager_stockMaterialLibrary.md)

## Version

Introduced in version September 2024  

