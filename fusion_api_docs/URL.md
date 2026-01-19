# URL Object

Derived from: [Base](Base.md) Object  

## Description

A URL object provides useful and easy-to-use methods for creating, modifying, and analyzing URLs.

## Methods

| Name | Description |
|----|----|
| [classType](URL_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [create](URL_create.md) | Create a new URL by given string. |
| [join](URL_join.md) | Join this URL with the given path and return the resulting URL. The operation does not alter the current URL. Join inserts a slash '/' to properly extend the path, so that "http://foo".join("bar") will return "http://foo/bar", not "http://foobar". |
| [toString](URL_toString.md) | Get the entire URL as string. |

## Properties

| Name | Description |
| --- | --- |
| [isURLValid](URL_isURLValid.md) | Check whether the URL is valid. Ensures that the URL is formatted with a protocol followed by a path which can be empty. The check is independent of the existence of the resource the URL may point to. |
| [isValid](URL_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [leafName](URL_leafName.md) | Get the leaf name of the URL, which is the section behind the last '/'. |
| [objectType](URL_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [parent](URL_parent.md) | Get the parent URL, represented by the section before the last '/'. |
| [pathName](URL_pathName.md) | Get the path name of the URL, including the last '/' of the protocol followed by the path of the URL. |
| [protocol](URL_protocol.md) | Get the protocol scheme of the URL, including the final ':'. |

## Accessed From

[CAMLibrary.childAssetURLs](CAMLibrary_childAssetURLs.md), [CAMLibrary.childFolderURLs](CAMLibrary_childFolderURLs.md), [CAMLibrary.createFolder](CAMLibrary_createFolder.md), [CAMLibrary.urlByLocation](CAMLibrary_urlByLocation.md), [CAMTemplateLibrary.childAssetURLs](CAMTemplateLibrary_childAssetURLs.md), [CAMTemplateLibrary.childFolderURLs](CAMTemplateLibrary_childFolderURLs.md), [CAMTemplateLibrary.createFolder](CAMTemplateLibrary_createFolder.md), [CAMTemplateLibrary.importTemplate](CAMTemplateLibrary_importTemplate.md), [CAMTemplateLibrary.updateTemplate](CAMTemplateLibrary_updateTemplate.md), [CAMTemplateLibrary.urlByLocation](CAMTemplateLibrary_urlByLocation.md), [Machine.postURL](Machine_postURL.md), [MachineFromLibraryInput.url](MachineFromLibraryInput_url.md), [MachineLibrary.childAssetURLs](MachineLibrary_childAssetURLs.md), [MachineLibrary.childFolderURLs](MachineLibrary_childFolderURLs.md), [MachineLibrary.createFolder](MachineLibrary_createFolder.md), [MachineLibrary.importMachine](MachineLibrary_importMachine.md), [MachineLibrary.urlByLocation](MachineLibrary_urlByLocation.md), [MachineQuery.url](MachineQuery_url.md), [PostConfigurationQuery.url](PostConfigurationQuery_url.md), [PostLibrary.childAssetURLs](PostLibrary_childAssetURLs.md), [PostLibrary.childFolderURLs](PostLibrary_childFolderURLs.md), [PostLibrary.createFolder](PostLibrary_createFolder.md), [PostLibrary.importPostConfiguration](PostLibrary_importPostConfiguration.md), [PostLibrary.urlByLocation](PostLibrary_urlByLocation.md), [PostProcessingMachineElement.postURL](PostProcessingMachineElement_postURL.md), [PrintSettingLibrary.childAssetURLs](PrintSettingLibrary_childAssetURLs.md), [PrintSettingLibrary.childFolderURLs](PrintSettingLibrary_childFolderURLs.md), [PrintSettingLibrary.createFolder](PrintSettingLibrary_createFolder.md), [PrintSettingLibrary.importPrintSetting](PrintSettingLibrary_importPrintSetting.md), [PrintSettingLibrary.urlByLocation](PrintSettingLibrary_urlByLocation.md), [PrintSettingQuery.url](PrintSettingQuery_url.md), [StockMaterialLibrary.childAssetURLs](StockMaterialLibrary_childAssetURLs.md), [StockMaterialLibrary.childFolderURLs](StockMaterialLibrary_childFolderURLs.md), [StockMaterialLibrary.createFolder](StockMaterialLibrary_createFolder.md), [StockMaterialLibrary.importStockMaterial](StockMaterialLibrary_importStockMaterial.md), [StockMaterialLibrary.urlByLocation](StockMaterialLibrary_urlByLocation.md), [ToolLibraries.childAssetURLs](ToolLibraries_childAssetURLs.md), [ToolLibraries.childFolderURLs](ToolLibraries_childFolderURLs.md), [ToolLibraries.createFolder](ToolLibraries_createFolder.md), [ToolLibraries.importToolLibrary](ToolLibraries_importToolLibrary.md), [ToolLibraries.urlByLocation](ToolLibraries_urlByLocation.md), [ToolQuery.url](ToolQuery_url.md), [ToolQueryResult.toolLibraryURL](ToolQueryResult_toolLibraryURL.md), [URL.create](URL_create.md), [URL.join](URL_join.md), [URL.parent](URL_parent.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

