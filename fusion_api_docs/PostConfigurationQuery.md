# PostConfigurationQuery Object

Derived from: [Base](Base.md) Object  

## Description

A PostConfigurationQuery can be used to search a LibraryLocation for a set of PostConfiguration objects matching the required properties.

## Methods

| Name | Description |
|----|----|
| [classType](PostConfigurationQuery_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |
| [execute](PostConfigurationQuery_execute.md) | Query for specific posts. This PostConfiguration query. |

## Properties

| Name | Description |
| --- | --- |
| [capability](PostConfigurationQuery_capability.md) | Specifies the capability to search for in the post library. |
| [isValid](PostConfigurationQuery_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [location](PostConfigurationQuery_location.md) | The location specifies the location to search in the post library. Setting the location clears any previous specified URL. |
| [objectType](PostConfigurationQuery_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [url](PostConfigurationQuery_url.md) | The URL specifies the location and folder to search for in the post library. Setting the URL updates the location. |
| [vendor](PostConfigurationQuery_vendor.md) | The case-insensitive vendor specifies the vendor of the post configuration. The default empty vendor applies to all post configurations. |

## Accessed From

[PostLibrary.createQuery](PostLibrary_createQuery.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

