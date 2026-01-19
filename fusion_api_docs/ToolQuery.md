# ToolQuery Object

Derived from: [Base](Base.md) Object  

## Description

ToolQuery objects are used to search for a set of Tools or ToolLibrary objects inside of the ToolLibraries collection or for a set of Tools inside of a particular ToolLibrary.

## Methods

| Name | Description |
|----|----|
| [classType](ToolQuery_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [execute](ToolQuery_execute.md) | Query for specific a Tool or ToolLbrary. |

## Properties

| Name | Description |
| --- | --- |
| [criteria](ToolQuery_criteria.md) | List of all criteria a tool must fulfill. Use the suffix '.min' and '.max', to define a upper and / or lower boundary for a particular value. |
| [isValid](ToolQuery_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [location](ToolQuery_location.md) | Specifies the location to search in the Tool library. Setting the location clears any previous specified URL. When searching inside a ToolLibrary the location will be ignored. |
| [objectType](ToolQuery_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [url](ToolQuery_url.md) | The URL specifies the location and folder to search for in the Tool library. Setting the URL updates the location. When searching inside a ToolLibrary the URL will be ignored. |
| [vendor](ToolQuery_vendor.md) | The case-insensitive vendor specifies the vendor of the tool. The default empty vendor applies to all tools. |

## Accessed From

[DocumentToolLibrary.createQuery](DocumentToolLibrary_createQuery.md), [ToolLibraries.createQuery](ToolLibraries_createQuery.md), [ToolLibrary.createQuery](ToolLibrary_createQuery.md)

## Samples

| Name | Description |
| --- | --- |
| [Hole and Pocket Recognition API Sample](HoleAndPocketRecognition_Sample.md) | This sample script demonstrates three different methods for feature recognition: one for holes and two for pockets. The script starts by creating a simple component which is then used to demonstrate the three methods. After the features are recognised they are coloured and milling and drilling operations are created for each feature. RecognizedHoleGroup returns a list of BRepFaces that can be used as selections for the drilling operation. RecognizedPocket also return some BRepFaces but it needs additional processing before the output can be used for creating machining operations. The sample script demonstrates a couple of different methods, including finding the pocket BRepFaces and creating sketches from the recognized pockets. This script works only if the Manufacturing Extension is active. |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

