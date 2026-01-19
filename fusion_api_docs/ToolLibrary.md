# ToolLibrary Object

Derived from: [Base](Base.md) Object  

## Description

ToolLibrary represents a collection of Tool objects.

## Methods

| Name | Description |
|----|----|
| [add](ToolLibrary_add.md) | Inserts a Tool at the end of the ToolLibrary. |
| [classType](ToolLibrary_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [createEmpty](ToolLibrary_createEmpty.md) | Creates an empty ToolLibrary. |
| [createFromJson](ToolLibrary_createFromJson.md) | Creates a ToolLibrary by given JSON-string. Raises an error if the given JSON is invalid. |
| [createQuery](ToolLibrary_createQuery.md) | Creates a new ToolQuery that is used to query the library for tools matching the query. |
| [item](ToolLibrary_item.md) | Get Tool by index in ToolLibrary. |
| [remove](ToolLibrary_remove.md) | Remove Tool by index from ToolLibrary. |
| [toJson](ToolLibrary_toJson.md) | Generate and return JSON string that contains all tools of that list. |

## Properties

| Name | Description |
| --- | --- |
| [count](ToolLibrary_count.md) | The number of tools in the ToolLibrary. |
| [isValid](ToolLibrary_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](ToolLibrary_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |

## Accessed From

[DocumentToolLibrary.createEmpty](DocumentToolLibrary_createEmpty.md), [DocumentToolLibrary.createFromJson](DocumentToolLibrary_createFromJson.md), [ToolLibraries.toolLibraryAtURL](ToolLibraries_toolLibraryAtURL.md), [ToolLibrary.createEmpty](ToolLibrary_createEmpty.md), [ToolLibrary.createFromJson](ToolLibrary_createFromJson.md), [ToolQueryResult.toolLibrary](ToolQueryResult_toolLibrary.md)

## Derived Classes

[DocumentToolLibrary](DocumentToolLibrary.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

