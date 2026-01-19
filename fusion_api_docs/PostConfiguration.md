# PostConfiguration Object

Derived from: [Base](Base.md) Object  

## Description

Object that represents a post configuration.

## Methods

| Name | Description |
|----|----|
| [classType](PostConfiguration_classType.md) | Static function that all classes support that returns the type of the class as a string. The returned string matches the string returned by the objectType property. For example if you have a reference to an object and you want to check if it's a SketchLine you can use myObject.objectType == fusion.SketchLine.classType(). |

## Properties

| Name | Description |
| --- | --- |
| [capability](PostConfiguration_capability.md) | Gets the capabilities supported by the post. Capabilities define what types of operations can be post processed using this configuration. |
| [description](PostConfiguration_description.md) | Gets the description of the post. |
| [extension](PostConfiguration_extension.md) | Gets the extension of the output file created by the post. |
| [isValid](PostConfiguration_isValid.md) | Indicates if this object is still valid, i.e. hasn't been deleted or some other action done to invalidate the reference. |
| [objectType](PostConfiguration_objectType.md) | This property is supported by all objects in the API and returns a string that contains the full name (namespace::objecttype) describing the type of the object. It's often useful to use this in combination with the classType method to see if an object is a certain type. For example: if obj.objectType == adsk.core.Point3D.classType(): |
| [vendor](PostConfiguration_vendor.md) | Gets the name of the vendor of the machine tool or controller this post configuration supports. |
| [version](PostConfiguration_version.md) | Gets the version of the post. |

## Accessed From

[NCProgram.postConfiguration](NCProgram_postConfiguration.md), [PostConfigurationQuery.execute](PostConfigurationQuery_execute.md), [PostLibrary.childPostConfigurations](PostLibrary_childPostConfigurations.md), [PostLibrary.postConfigurationAtURL](PostLibrary_postConfigurationAtURL.md)

## Samples

| Name | Description |
| --- | --- |
| [Manufacturing Workflow API Sample](ManufacturingWorkflowAPISample_Sample.md) | Manufacturing Workflow API Sample This sample script starts by creating a simple component which is then used to describe a milling workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |
| [Turning Workflow API Sample](Turning_Workflow_API_Sample_Sample.md) | Turning Workflow API Sample This sample script starts by opening a simple component which is then used to describe a basic turning workflow. It creates a setup, a few operations, pick some tools from a Fusion sample tool library using loops and queries and ends up post-processing the operations out using an NC Program. |

## Version

Introduced in version April 2023  

